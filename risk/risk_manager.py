from config.settings import RISK_RULES

class RiskManager:
    def __init__(self):
        self.rules = RISK_RULES

    def validate_trade(self, portfolio_balance, trade_amount, daily_loss_pct):
        """Validate if a trade meets risk management rules."""
        # Rule 1: Max position size (5%)
        max_pos_size = portfolio_balance * self.rules['max_position_size']
        if trade_amount > max_pos_size:
            return False, f"Trade amount {trade_amount} exceeds max position size {max_pos_size}"

        # Rule 2: Max daily loss (10%)
        if daily_loss_pct > self.rules['max_daily_loss']:
            return False, f"Daily loss {daily_loss_pct} exceeds max daily loss {self.rules['max_daily_loss']}"

        return True, "Trade validated"

    def calculate_stop_loss(self, entry_price, side, stop_loss_pct=0.02):
        """Calculate stop loss price based on entry price and side."""
        if side == "BUY":
            return entry_price * (1 - stop_loss_pct)
        elif side == "SELL":
            return entry_price * (1 + stop_loss_pct)
        return None

    def calculate_take_profit(self, entry_price, side, take_profit_pct=0.05):
        """Calculate take profit price based on entry price and side."""
        if side == "BUY":
            return entry_price * (1 + take_profit_pct)
        elif side == "SELL":
            return entry_price * (1 - take_profit_pct)
        return None
