
from services.logger import setup_logger
from utils.cyan_message import cyan_message
from utils.is_pumpfun_token import is_pumpfun_token


logger = setup_logger("RUGCHECKER")


class RugCheck:
    def __init__(self, enabled=True, is_rugged=True, is_pumpFun=True, risks=None):
        self.enabled = enabled
        self.is_rugged = is_rugged
        self.is_pumpFun = is_pumpFun
        self.risks = risks or {}  # Default to an empty dictionary if None

    def is_valid(self, token, rugcheck_report):

        if not self.enabled:
            return True  # Filtering disabled, allow all tokens

        # Validate RugCheck report structure
        if not isinstance(rugcheck_report, dict) or not isinstance(rugcheck_report.get("data", {}), dict):
            logger.error(f"Token {token} - Invalid RugCheck report format.")
            return False

        # Check if RugCheck API returned a valid response
        if rugcheck_report is False:
            logger.warning(f"Token {token} - RugCheck failed or disabled.")
            return False

        # Check if token is rugged
        is_rugged = rugcheck_report.get("data", {}).get("rugged", True)
        if is_rugged and not self.is_rugged:
            logger.warning(f"Token {token} - Is rugged! Skipping due to settings.")
            return False

        # Check if it's a PumpFun token
        if is_pumpfun_token(token) and not self.is_pumpFun:
            logger.warning(f"Token {token} - Is a Pump.fun token! Skipping due to settings.")
            return False

        # Check for specific risks in the RugCheck report
        risks = rugcheck_report.get("data", {}).get("risk", {}).get("risks", [])
        for risk in risks:
            risk_name = risk.get("name")
            risk_score = risk.get("score", 0)

            # Check if this risk is enabled and if the score exceeds the threshold
            risk_config = self.risks.get(risk_name, {})
            if risk_config.get("enabled", False) and risk_score >= risk_config.get("score_threshold", 0):
                logger.warning(
                    f"Token {token} - Risk '{risk_name}' detected! "
                    f"Score: {risk_score} (threshold: {risk_config.get('score_threshold', 0)}). "
                    "Skipping due to settings."
                )
                return False

        return True  # Token passed all checks