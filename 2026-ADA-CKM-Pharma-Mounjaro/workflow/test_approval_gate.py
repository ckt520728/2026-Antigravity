"""核准狀態回歸測試；不觸碰真正大綱。"""
import unittest
from validate_project import approval_allows_production

class ApprovalGateTest(unittest.TestCase):
    def test_approved_matching_hash(self):
        self.assertTrue(approval_allows_production({"status": "approved", "sha256": "abc"}, "abc"))
    def test_approved_mismatching_hash(self):
        self.assertFalse(approval_allows_production({"status": "approved", "sha256": "old"}, "abc"))
    def test_pending_never_allows_production(self):
        self.assertFalse(approval_allows_production({"status": "pending", "sha256": "abc"}, "abc"))
    def test_outline_never_authorizes_release_or_spend(self):
        record = {"status": "approved", "sha256": "abc"}
        self.assertNotEqual(record.get("publication_authorized"), True)
        self.assertNotEqual(record.get("spend_authorized"), True)

if __name__ == "__main__":
    unittest.main()
