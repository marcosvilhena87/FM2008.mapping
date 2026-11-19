import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_player_identification.py"
spec = importlib.util.spec_from_file_location("verification", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.observed = [{
            "save_id": "save-02", "index": "4", "id": "107",
            "first_name": "Alexander", "last_name": "Östlund", "common_name": ""
        }]
        self.reference = [{
            "save_id": "save-02", "observed_index": "4", "reference_id": "",
            "first_name": "Alexander", "last_name": "Ostlund", "common_name": "",
            "source_type": "game_ui",
            "source_detail": "Perfil do jogador aberto no FM2008, segunda partida",
            "reviewer": "Revisor"
        }]

    def status(self):
        return module.verify(self.observed, self.reference)["entries"][0]["status"]

    def test_name_only_from_game(self):
        self.assertEqual("name_only", self.status())

    def test_unreviewed_template_pending(self):
        self.reference[0]["reviewer"] = ""
        self.assertEqual("pending", self.status())

    def test_placeholder_pending(self):
        self.reference[0]["source_detail"] = "Confirmar no perfil do jogador (nome somente)"
        self.assertEqual("pending", self.status())

    def test_probe_is_not_independent(self):
        self.reference[0]["source_type"] = "same_probe"
        self.assertEqual("pending", self.status())

    def test_copy_from_probe_rejected(self):
        self.reference[0]["source_detail"] = "Texto do ReadOnlyProbe"
        self.assertEqual("pending", self.status())

    def test_game_ui_cannot_confirm_id(self):
        self.reference[0]["reference_id"] = "107"
        self.assertEqual("name_only", self.status())

    def test_independent_id_and_name(self):
        self.reference[0]["reference_id"] = "107"
        self.reference[0]["source_type"] = "independent_database"
        self.reference[0]["source_detail"] = "Registo DB de origem distinta conferido"
        result = module.verify(self.observed, self.reference)
        self.assertEqual("id_and_name_match", result["entries"][0]["status"])
        self.assertTrue(result["all_ids_independently_confirmed"])
        self.assertFalse(result["approved"])
        self.assertFalse(result["operational"])

    def test_id_explicitly_visible_in_game_ui(self):
        self.reference[0]["source_type"] = "game_ui_id_visible"
        self.reference[0]["reference_id"] = "107"
        self.reference[0]["source_detail"] = "ID 107 e nome vistos diretamente no perfil do FM2008"
        result = module.verify(self.observed, self.reference)
        self.assertEqual("id_and_name_match", result["entries"][0]["status"])
        self.assertEqual(1, result["independently_confirmed_ids"])
        self.assertFalse(result["approved"])

    def test_game_ui_id_disagreement(self):
        self.reference[0]["source_type"] = "game_ui_id_visible"
        self.reference[0]["reference_id"] = "999"
        self.assertEqual("mismatch", self.status())

    def test_independent_id_mismatch(self):
        self.reference[0]["reference_id"] = "999"
        self.reference[0]["source_type"] = "independent_tool"
        self.assertEqual("mismatch", self.status())

    def test_name_mismatch(self):
        self.reference[0]["last_name"] = "Outro"
        self.assertEqual("mismatch", self.status())

    def test_duplicate_observation_rejected(self):
        with self.assertRaises(ValueError):
            module.verify(self.observed * 2, self.reference)

    def test_duplicate_reference_rejected(self):
        with self.assertRaises(ValueError):
            module.verify(self.observed, self.reference * 2)

    def test_unmatched_reference_rejected(self):
        self.reference[0]["observed_index"] = "42"
        with self.assertRaises(ValueError):
            module.verify(self.observed, self.reference)


if __name__ == "__main__":
    unittest.main()
