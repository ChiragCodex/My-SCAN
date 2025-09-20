"""
screener_conditions.py
-----------------------
Purpose:
    Stores Chartink screener conditions for filtering stocks.

Contains:
    - GAINER_CONDITION : String defining rules to identify gainers.
    - LOSER_CONDITION  : String defining rules to identify losers.

Editable:
    - Update the conditions here if you want to change your stock scanning logic.
"""


GAINER_CONDITION = """
( {33489}
    ( {33489}
        ( [=1] 1 hour close > [=1] 1 hour open
          and [=1] 1 hour close > [=-1] 3 hour high
          and fno lot size <= 8000
          and [=1] 1 hour volume >= 50000 )
    )
    
    and ( {33489}
        ( [=1] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7
          and [=2] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7
          and [=3] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7
          and [=4] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7 )
    )
    
    and ( {33489}
        ( [=3] 15 minute rsi( 8 ) > [=3] 15 minute ema( [=3] 15 minute rsi( 8 ), 8 )
          and [=4] 15 minute rsi( 8 ) > [=4] 15 minute ema( [=4] 15 minute rsi( 8 ), 8 )
          and [=1] 1 hour rsi( 8 ) > [=1] 1 hour ema( [=1] 1 hour rsi( 8 ), 8 ) )
    )
    
    and ( {33489}
        ( ( [=1] 1 hour close - [=1] 1 hour low ) / ( [=1] 1 hour high - [=1] 1 hour low ) > 0.62
          and ( [=1] 1 hour high - [=1] 1 hour low ) > ( [=1] 1 hour sma( [=1] 1 hour high - [=1] 1 hour low, 17 ) * 1.7 )
          and abs( [=1] 1 hour close - [=1] 1 hour open ) / ( [=1] 1 hour high - [=1] 1 hour low ) < 1 )
    )
    
    and ( {33489}
        ( [=1] 1 hour obv > [=1] 1 hour wma( [=1] 1 hour obv, 8 ) and [=-1] 1 hour obv <= [=-1] 1 hour wma( [=-1] 1 hour obv, 8 )
          or [=-1] 1 hour obv > [=-1] 1 hour wma( [=-1] 1 hour obv, 8 ) and [=-2] 1 hour obv <= [=-2] 1 hour wma( [=-2] 1 hour obv, 8 )
          or [=-2] 1 hour obv > [=-2] 1 hour wma( [=-2] 1 hour obv, 8 ) and [=-3] 1 hour obv <= [=-3] 1 hour wma( [=-3] 1 hour obv, 8 ) )
    )
    
    and ( {33489}
        ( [=1] 1 hour cci( 17 ) > -86 and [=-1] 1 hour cci( 17 ) <= -86
          or [=1] 1 hour cci( 17 ) > 86 and [=-1] 1 hour cci( 17 ) <= 86
          or [=1] 1 hour cci( 17 ) > -100 and [=-1] 1 hour cci( 17 ) <= -100
          or [=1] 1 hour cci( 17 ) > 100 and [=-1] 1 hour cci( 17 ) <= 100)
    )
    
    and ( {33489}
        ( [=1] 1 hour rsi( 8 ) > 68 and [=-1] 1 hour rsi( 8 ) <= 68
          or [=1] 1 hour rsi( 8 ) > 30 and [=-1] 1 hour rsi( 8 ) <= 30
          or [=-1] 1 hour rsi( 8 ) > 68 and [=-2] 1 hour rsi( 8 ) <= 68
          or [=-2] 1 hour rsi( 8 ) > 68 and [=-3] 1 hour rsi( 8 ) <= 68
          or [=1] 1 hour rsi( 8 ) > 78.2 and [=-1] 1 hour rsi( 8 ) >= 70)
    )
    
    and ( {33489}
        ( [=1] 1 hour wma( [=1] 1 hour close, 17 ) > [=1] 1 hour low and [=1] 1 hour wma( [=1] 1 hour close, 17 ) < [=1] 1 hour close
          or [=1] 1 hour wma( [=1] 1 hour close, 17 ) < [=1] 1 hour close and [=-1] 1 hour wma( [=1] 1 hour close, 17 ) >= [=-1] 1 hour close )
    )
    
    and ( {33489}
        ( [=3] 15 minute close > [=3] 15 minute supertrend( 17, 1.7 )
          and [=4] 15 minute close > [=4] 15 minute supertrend( 17, 1.7 )
          and [=1] 1 hour close > [=1] 1 hour supertrend( 17, 1.7 ) )
    )
)
"""


LOSER_CONDITION = """
( {33489}
    ( {33489}
        ( [=1] 1 hour close < [=1] 1 hour open
          and [=1] 1 hour close < [=-1] 3 hour low
          and fno lot size <= 8000
          and [=1] 1 hour volume >= 50000 )
    )
    
    and ( {33489}
        ( [=1] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7
          and [=2] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7
          and [=3] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7
          and [=4] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7 )
    )
    
    and ( {33489}
        ( [=3] 15 minute rsi( 8 ) <= [=3] 15 minute ema( [=3] 15 minute rsi( 8 ), 8 )
          and [=4] 15 minute rsi( 8 ) <= [=4] 15 minute ema( [=4] 15 minute rsi( 8 ), 8 )
          and [=1] 1 hour rsi( 8 ) <= [=1] 1 hour ema( [=1] 1 hour rsi( 8 ), 8 ) )
    )
    
    and ( {33489}
        ( abs( [=1] 1 hour close - [=1] 1 hour high ) / ( [=1] 1 hour high - [=1] 1 hour low ) > 0.62
          and ( [=1] 1 hour high - [=1] 1 hour low ) > ( [=1] 1 hour sma( [=1] 1 hour high - [=1] 1 hour low, 17 ) * 1.7 )
          and abs( [=1] 1 hour open - [=1] 1 hour close ) / ( [=1] 1 hour high - [=1] 1 hour low ) < 1 )
    )
    
    and ( {33489}
        ( [=1] 1 hour obv < [=1] 1 hour wma( [=1] 1 hour obv, 8 ) and [=-1] 1 hour obv >= [=-1] 1 hour wma( [=-1] 1 hour obv, 8 )
          or [=-1] 1 hour obv < [=-1] 1 hour wma( [=-1] 1 hour obv, 8 ) and [=-2] 1 hour obv >= [=-2] 1 hour wma( [=-2] 1 hour obv, 8 )
          or [=-2] 1 hour obv < [=-2] 1 hour wma( [=-2] 1 hour obv, 8 ) and [=-3] 1 hour obv >= [=-3] 1 hour wma( [=-3] 1 hour obv, 8 ) )
    )
    
    and ( {33489}
        ( [=1] 1 hour cci( 17 ) < -86 and [=-1] 1 hour cci( 17 ) >= -86
          or [=1] 1 hour cci( 17 ) < 86 and [=-1] 1 hour cci( 17 ) >= 86
          or [=1] 1 hour cci( 17 ) < -100 and [=-1] 1 hour cci( 17 ) >= -100
          or [=1] 1 hour cci( 17 ) < 100 and [=-1] 1 hour cci( 17 ) >= 100)
    )
    
    and ( {33489}
        ( [=1] 1 hour rsi( 8 ) < 32 and [=-1] 1 hour rsi( 8 ) >= 32
          or [=-1] 1 hour rsi( 8 ) < 32 and [=-2] 1 hour rsi( 8 ) >= 32
          or [=-2] 1 hour rsi( 8 ) < 32 and [=-3] 1 hour rsi( 8 ) >= 32
          or [=1] 1 hour rsi( 8 ) < 70 and [=-1] 1 hour rsi( 8 ) >= 70
          or [=1] 1 hour rsi( 8 ) < 20 and [=-1] 1 hour rsi( 8 ) <= 30)
    )
    
    and ( {33489}
        ( [=1] 1 hour wma( [=1] 1 hour close, 17 ) < [=1] 1 hour high and [=1] 1 hour wma( [=1] 1 hour close, 17 ) > [=1] 1 hour close
          or [=1] 1 hour wma( [=1] 1 hour close, 17 ) > [=1] 1 hour close and [=-1] 1 hour wma( [=1] 1 hour close, 17 ) <= [=-1] 1 hour close )
    )
    
    and ( {33489}
        ( [=3] 15 minute close < [=3] 15 minute supertrend( 17, 1.7 )
          and [=4] 15 minute close < [=4] 15 minute supertrend( 17, 1.7 )
          and [=1] 1 hour close < [=1] 1 hour supertrend( 17, 1.7 ) )
    )
)
"""
