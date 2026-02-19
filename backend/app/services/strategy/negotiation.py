"""
Negotiation engine that determines optimal strategy based on
debtor profile, emotional state, and conversation progress.
"""

from dataclasses import dataclass
import structlog

logger = structlog.get_logger()


@dataclass
class NegotiationContext:
    original_amount: float
    negotiable_amount: float
    days_past_due: int
    risk_profile: str
    emotional_state: str
    current_strategy: str
    turn_count: int = 0


@dataclass
class NegotiationAction:
    strategy: str
    offer_amount: float | None
    talking_points: list[str]
    tone: str
    urgency_level: str  # low, medium, high


class NegotiationEngine:
    """
    Determines the best negotiation approach based on context.

    The engine considers the debtor's emotional state, risk profile,
    and conversation progress to recommend actions.
    """

    def determine_action(self, context: NegotiationContext) -> NegotiationAction:
        strategy = self._select_strategy(context)
        offer = self._calculate_offer(context)
        points = self._generate_talking_points(context, strategy)
        tone = self._determine_tone(context)
        urgency = self._assess_urgency(context)

        action = NegotiationAction(
            strategy=strategy,
            offer_amount=offer,
            talking_points=points,
            tone=tone,
            urgency_level=urgency,
        )

        logger.info(
            "negotiation_action",
            strategy=strategy,
            offer=offer,
            tone=tone,
            urgency=urgency,
        )
        return action

    def _select_strategy(self, ctx: NegotiationContext) -> str:
        if ctx.emotional_state == "aggressive":
            return "empathetic"
        if ctx.emotional_state == "anxious":
            return "empathetic"
        if ctx.emotional_state == "evasive":
            return "informative"
        if ctx.emotional_state == "defensive":
            return "informative"
        if ctx.emotional_state == "cooperative":
            if ctx.turn_count > 3:
                return "firm"
            return ctx.current_strategy
        return ctx.current_strategy

    def _calculate_offer(self, ctx: NegotiationContext) -> float | None:
        if ctx.turn_count < 2:
            return None  # too early to make an offer

        discount_factor = 1.0
        if ctx.days_past_due > 365:
            discount_factor = 0.4
        elif ctx.days_past_due > 180:
            discount_factor = 0.55
        elif ctx.days_past_due > 90:
            discount_factor = 0.7
        else:
            discount_factor = 0.85

        if ctx.risk_profile == "high":
            discount_factor *= 0.85
        elif ctx.risk_profile == "low":
            discount_factor *= 1.1

        offer = max(ctx.negotiable_amount, ctx.original_amount * discount_factor)
        return round(offer, 2)

    def _generate_talking_points(
        self, ctx: NegotiationContext, strategy: str
    ) -> list[str]:
        points = []

        if strategy == "empathetic":
            points.append(
                "Acknowledge the difficulty of the situation."
            )
            points.append(
                "Mention that many people in similar situations have found resolution."
            )
        elif strategy == "informative":
            savings = ctx.original_amount - ctx.negotiable_amount
            points.append(
                f"The current program allows a reduction of up to ${savings:.2f}."
            )
            points.append(
                "Explain the legal framework that enables this reduction."
            )
        elif strategy == "firm":
            points.append(
                "Present the offer clearly with specific terms."
            )
            points.append(
                "Explain the timeline for resolution."
            )
        elif strategy == "urgent":
            points.append(
                "Mention that this offer has a specific validity period."
            )
            points.append(
                "Contrast current offer with what would happen without resolution."
            )

        return points

    def _determine_tone(self, ctx: NegotiationContext) -> str:
        tone_map = {
            "aggressive": "calm_professional",
            "anxious": "warm_reassuring",
            "cooperative": "friendly_professional",
            "evasive": "patient_persistent",
            "defensive": "transparent_respectful",
        }
        return tone_map.get(ctx.emotional_state, "professional")

    def _assess_urgency(self, ctx: NegotiationContext) -> str:
        if ctx.days_past_due > 300:
            return "high"
        if ctx.days_past_due > 150:
            return "medium"
        return "low"
