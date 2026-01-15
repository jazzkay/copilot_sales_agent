from data.crm_data import CRM_DATA
from data.meeting_notes import MEETING_NOTES
from data.templates import PROPOSAL_TEMPLATE

class SalesProposalAgent:
    def __init__(self):
        self.state = {
            "proposal_stage": "initiated",
            "customer": None,
            "approvals": {
                "finance": "pending",
                "sales_manager": "pending"
            },
            "proposal_text": None
        }

    def analyze_request(self, user_input):
        self.state["customer"] = "ACME Corp"
        return {
            "intent": "create_or_update_proposal",
            "customer": self.state["customer"]
        }

    def gather_context(self):
        customer = self.state["customer"]
        crm_info = CRM_DATA.get(customer, {})
        meeting_info = MEETING_NOTES.get(customer, "")
        return crm_info, meeting_info

    def build_assumptions(self):
        assumptions = []

        if self.state["approvals"]["finance"] == "pending":
            assumptions.append("Pricing is provisional and subject to Finance approval.")

        if self.state["approvals"]["sales_manager"] == "pending":
            assumptions.append("Proposal content is pending Sales Manager review.")

        assumptions.append("Scope is based on the most recent client meeting discussion.")

        return "\n".join(f"• {a}" for a in assumptions)

    def generate_proposal(self, crm_info, meeting_info):
        assumptions_text = self.build_assumptions()

        proposal = PROPOSAL_TEMPLATE.format(
            company=self.state["customer"],
            industry=crm_info.get("industry", "N/A"),
            deal_value=crm_info.get("deal_value", "N/A"),
            background=meeting_info,
            assumptions=assumptions_text
        )

        self.state["proposal_text"] = proposal
        self.state["proposal_stage"] = "drafted"

        return proposal

    def revise_proposal(self, instruction):
        if not self.state["proposal_text"]:
            return None

        revised = self.state["proposal_text"]

        if "technical" in instruction.lower():
            revised += "\n\nTECHNICAL NOTES\n• Solution integrates with enterprise CRM and analytics systems."

        if "shorten background" in instruction.lower():
            revised = revised.replace(
                "BACKGROUND",
                "BACKGROUND (Condensed)"
            )

        self.state["proposal_text"] = revised
        self.state["proposal_stage"] = "revised"

        return revised

    def approvals_pending(self):
        return any(status == "pending" for status in self.state["approvals"].values())

    def plan_actions(self):
        actions = [
            "Fetched CRM data",
            "Retrieved meeting summary",
            "Selected proposal template"
        ]

        if self.state["proposal_stage"] == "drafted":
            actions.append("Drafted proposal")

        if self.state["proposal_stage"] == "revised":
            actions.append("Revised proposal based on feedback")

        if self.approvals_pending():
            actions.append("Waiting for required approvals")

        return actions

    def approve(self, role):
        if role in self.state["approvals"]:
            self.state["approvals"][role] = "approved"
