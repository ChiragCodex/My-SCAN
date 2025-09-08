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
        ( {33489}
            ( [=1] 1 hour close > [=1] 1 hour open
              and [=3] 15 minute rsi( 8 ) > [=3] 15 minute ema( [=3] 15 minute rsi( 8 ) , 8 )
              and [=4] 15 minute rsi( 8 ) > [=4] 15 minute ema( [=4] 15 minute rsi( 8 ) , 8 )
              and [=1] 1 hour rsi( 26 ) > [=1] 1 hour ema( [=1] 1 hour rsi( 26 ) , 26 )
              and [=4] 15 minute close > [=4] 15 minute supertrend( 17 , 1.7 )
              and [=3] 15 minute close > [=3] 15 minute supertrend( 17 , 1.7 )
              and [=1] 1 hour volume >= 10000
              and [=4] 15 minute rsi( 8 ) >= 50
              and [=3] 15 minute rsi( 8 ) >= 50
              and [=1] 1 hour rsi( 8 ) >= 44
              and [=3] 15 minute close >= [=3] 15 minute ema( [=3] 15 minute close , 26 )
              and [=4] 15 minute close >= [=4] 15 minute ema( [=4] 15 minute close , 26 ) )
        )
        and ( {33489}
            ( [=1] 20 minute close > ( ( [=1] 20 minute ema( [=1] 20 minute close , 62 ) + [=1] 20 minute "wma( ( ( 2 * wma( ([=1] 20 minute close), 11) ) - wma(([=1] 20 minute close), 22) ), 4)" ) / 2 ) + [=1] 20 minute sma( ( [=1] 20 minute high - [=1] 20 minute low ) , 200 ) / 2
              and [=2] 20 minute close > ( ( [=2] 20 minute ema( [=2] 20 minute close , 62 ) + [=2] 20 minute "wma( ( ( 2 * wma( ([=2] 20 minute close), 11) ) - wma(([=2] 20 minute close), 22) ), 4)" ) / 2 ) + [=2] 20 minute sma( ( [=2] 20 minute high - [=2] 20 minute low ) , 200 ) / 2
              and [=3] 20 minute close > ( ( [=3] 20 minute ema( [=3] 20 minute close , 62 ) + [=3] 20 minute "wma( ( ( 2 * wma( ([=3] 20 minute close), 11) ) - wma(([=3] 20 minute close), 22) ), 4)" ) / 2 ) + [=3] 20 minute sma( ( [=3] 20 minute high - [=3] 20 minute low ) , 200 ) / 2 )
        )
        and ( {33489}
            ( [=1] 1 hour close > [=-1] 3 hour high
              and [=1] 1 hour close > [=1] 15 minute high )
        )
        and ( {33489}
            ( [=1] 1 hour close > ( ( 1 day ago high + 1 day ago low + 1 day ago close ) / 1.5 ) - ( ( 1 day ago high + 1 day ago low ) / 2 )
              and [=1] 1 hour close > ( 1 day ago high + 1 day ago low ) / 2 )
        )
        and ( {33489} ( fno lot size <= 8000 ) )
        and ( {33489}
            ( [=3] 15 minute wma( [=3] 15 minute close , 17 ) < [=3] 15 minute close
              and [=3] 15 minute wma( [=3] 15 minute close , 17 ) < [=3] 15 minute low
              and [=4] 15 minute wma( [=4] 15 minute close , 17 ) < [=4] 15 minute close
              and [=4] 15 minute wma( [=4] 15 minute close , 17 ) < [=4] 15 minute low
              and [=1] 1 hour wma( [=1] 1 hour close , 8 ) < [=1] 1 hour close
              and [=1] 1 hour wma( [=1] 1 hour close , 8 ) > [=1] 1 hour low )
        )
        and ( {33489}
            ( [=1] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7
              and [=2] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7
              and [=3] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7
              and [=4] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" <= 1.7 )
        )
        and ( {33489}
            ( {33489}
                ( [=1] 15 minute obv > [=1] 15 minute ema( [=1] 15 minute obv , 8 ) and [ =-1 ] 15 minute obv < [ =-1 ] 15 minute ema( [=1] 15 minute obv , 8 )
                  or [=2] 15 minute obv > [=2] 15 minute ema( [=2] 15 minute obv , 8 ) and [ =1 ] 15 minute obv < [ =1 ] 15 minute ema( [=2] 15 minute obv , 8 )
                  or [=-1] 15 minute obv > [=-1] 15 minute ema( [=-1] 15 minute obv , 5 ) and [ =-2 ] 15 minute obv < [ =-2 ] 15 minute ema( [=-1] 15 minute obv , 5 )
                  or [=-2] 15 minute obv > [=-2] 15 minute ema( [=-2] 15 minute obv , 5 ) and [ =-3 ] 15 minute obv > [ =-3 ] 15 minute ema( [=-2] 15 minute obv , 5 )
                  or [=-3] 15 minute obv > [=-3] 15 minute ema( [=-3] 15 minute obv , 5 ) and [ =-4 ] 15 minute obv < [ =-4 ] 15 minute ema( [=-3] 15 minute obv , 5 ) )
            )
            and ( {33489}
                ( [=1] 15 minute cci( 26 ) > -100 and [ =-1 ] 15 minute cci( 26 ) <= -100
                  or [=2] 15 minute cci( 26 ) > -100 and [ =1 ] 15 minute cci( 26 ) <= -100
                  or [=3] 15 minute cci( 26 ) > -100 and [ =2 ] 15 minute cci( 26 ) <= -100
                  or [=-1] 15 minute cci( 26 ) > -100 and [ =-2 ] 15 minute cci( 26 ) >= -100
                  or [=-2] 15 minute cci( 26 ) > -100 and [ =-3 ] 15 minute cci( 26 ) >= -100
                  or [=-3] 15 minute cci( 26 ) > -100 and [ =-4 ] 15 minute cci( 26 ) >= -100 )
            )
            or ( {33489}
                ( [=1] 15 minute cci( 26 ) > 100 and [ =-1 ] 15 minute cci( 26 ) <= 100
                  or [=2] 15 minute cci( 26 ) > 100 and [ =1 ] 15 minute cci( 26 ) <= 100
                  or [=3] 15 minute cci( 26 ) > 100 and [ =2 ] 15 minute cci( 26 ) <= 100
                  or [=-1] 15 minute cci( 26 ) > 100 and [ =-2 ] 15 minute cci( 26 ) <= 100
                  or [=-2] 15 minute cci( 26 ) > 100 and [ =-3 ] 15 minute cci( 26 ) >= 100
                  or [=-3] 15 minute cci( 26 ) > 100 and [ =-4 ] 15 minute cci( 26 ) >= 100 )
            )
        )
    )
)
"""
LOSER_CONDITION = """
( {33489}
    ( {33489}
        ( {33489}
            ( [=1] 1 hour close < [=1] 1 hour open
              and [=3] 15 minute rsi( 8 ) < [=3] 15 minute ema( [=3] 15 minute rsi( 8 ) , 8 )
              and [=4] 15 minute rsi( 8 ) < [=4] 15 minute ema( [=4] 15 minute rsi( 8 ) , 8 )
              and [=1] 1 hour rsi( 26 ) < [=1] 1 hour ema( [=1] 1 hour rsi( 26 ) , 26 )
              and [=4] 15 minute close < [=4] 15 minute supertrend( 17 , 1.7 )
              and [=3] 15 minute close < [=3] 15 minute supertrend( 17 , 1.7 )
              and [=1] 1 hour volume >= 10000
              and [=4] 15 minute rsi( 8 ) <= 50
              and [=3] 15 minute rsi( 8 ) <= 50
              and [=1] 1 hour rsi( 8 ) <= 55
              and [=3] 15 minute close <= [=3] 15 minute ema( [=3] 15 minute close , 26 )
              and [=4] 15 minute close <= [=4] 15 minute ema( [=4] 15 minute close , 26 ) )
        )
        and ( {33489}
            ( [=1] 20 minute close < ( ( [=1] 20 minute ema( [=1] 20 minute close , 62 ) + [=1] 20 minute "wma( ( ( 2 * wma( ([=1] 20 minute close), 11) ) - wma(([=1] 20 minute close), 22) ), 4)" ) / 2 )
              and [=2] 20 minute close < ( ( [=2] 20 minute ema( [=2] 20 minute close , 62 ) + [=2] 20 minute "wma( ( ( 2 * wma( ([=2] 20 minute close), 11) ) - wma(([=2] 20 minute close), 22) ), 4)" ) / 2 )
              and [=3] 20 minute close < ( ( [=3] 20 minute ema( [=3] 20 minute close , 62 ) + [=3] 20 minute "wma( ( ( 2 * wma( ([=3] 20 minute close), 11) ) - wma(([=3] 20 minute close), 22) ), 4)" ) / 2 ) )
        )
        and ( {33489}
            ( [=1] 1 hour close < [=-1] 3 hour low
              and [=1] 1 hour close < [=1] 15 minute low )
        )
        and ( {33489}
            ( [=1] 1 hour close < ( ( 1 day ago high + 1 day ago low + 1 day ago close ) / 1.5 ) - ( ( 1 day ago high + 1 day ago low ) / 2 )
              and [=1] 1 hour close < ( 1 day ago high + 1 day ago low ) / 2 )
        )
        and ( {33489}
            ( [=3] 15 minute obv <= [=3] 15 minute ema( [=3] 15 minute obv , 8 )
              and [=4] 15 minute obv <= [=4] 15 minute ema( [=4] 15 minute obv , 8 ) )
        )
        and ( {33489} ( fno lot size <= 8000 ) )
        and ( {33489}
            ( [=3] 15 minute wma( [=3] 15 minute close , 17 ) > [=3] 15 minute close
              and [=3] 15 minute wma( [=3] 15 minute close , 17 ) > [=3] 15 minute high
              and [=4] 15 minute wma( [=4] 15 minute close , 17 ) > [=4] 15 minute close
              and [=4] 15 minute wma( [=4] 15 minute close , 17 ) > [=4] 15 minute high
              and [=1] 1 hour wma( [=1] 1 hour close , 8 ) > [=1] 1 hour close
              and [=1] 1 hour wma( [=1] 1 hour close , 8 ) < [=1] 1 hour high )
        )
        and ( {33489}
            ( [=1] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7
              and [=2] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7
              and [=3] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7
              and [=4] 15 minute "close - 1 candle ago close / 1 candle ago close * 100" >= -1.7 )
        )
        and ( {33489}
            ( {33489}
                ( [=1] 15 minute obv < [=1] 15 minute ema( [=1] 15 minute obv , 8 ) and [ =-1 ] 15 minute obv > [ =-1 ] 15 minute ema( [=1] 15 minute obv , 8 )
                  or [=2] 15 minute obv < [=2] 15 minute ema( [=2] 15 minute obv , 8 ) and [ =1 ] 15 minute obv > [ =1 ] 15 minute ema( [=2] 15 minute obv , 8 )
                  or [=-1] 15 minute obv < [=-1] 15 minute ema( [=-1] 15 minute obv , 5 ) and [ =-2 ] 15 minute obv > [ =-2 ] 15 minute ema( [=-1] 15 minute obv , 5 )
                  or [=-2] 15 minute obv < [=-2] 15 minute ema( [=-2] 15 minute obv , 5 ) and [ =-3 ] 15 minute obv > [ =-3 ] 15 minute ema( [=-2] 15 minute obv , 5 )
                  or [=-3] 15 minute obv < [=-3] 15 minute ema( [=-3] 15 minute obv , 5 ) and [ =-4 ] 15 minute obv > [ =-4 ] 15 minute ema( [=-3] 15 minute obv , 5 ))
            )
            and ( {33489}
                ( [=1] 15 minute cci( 26 ) < -100 and [ =-1 ] 15 minute cci( 26 ) >= -100
                  or [=2] 15 minute cci( 26 ) < -100 and [ =1 ] 15 minute cci( 26 ) >= -100
                  or [=3] 15 minute cci( 26 ) < -100 and [ =2 ] 15 minute cci( 26 ) >= -100
                  or [=-1] 15 minute cci( 26 ) < -100 and [ =-2 ] 15 minute cci( 26 ) >= -100
                  or [=-2] 15 minute cci( 26 ) < -100 and [ =-3 ] 15 minute cci( 26 ) >= -100
                  or [=-3] 15 minute cci( 26 ) < -100 and [ =-4 ] 15 minute cci( 26 ) >= -100 )
            )
            or ( {33489}
                ( [=1] 15 minute cci( 26 ) < 100 and [ =-1 ] 15 minute cci( 26 ) >= 100
                  or [=2] 15 minute cci( 26 ) < 100 and [ =1 ] 15 minute cci( 26 ) >= 100
                  or [=3] 15 minute cci( 26 ) < 100 and [ =2 ] 15 minute cci( 26 ) >= 100
                  or [=-1] 15 minute cci( 26 ) < 100 and [ =-2 ] 15 minute cci( 26 ) >= 100
                  or [=-2] 15 minute cci( 26 ) < 100 and [ =-3 ] 15 minute cci( 26 ) >= 100
                  or [=-3] 15 minute cci( 26 ) < 100 and [ =-4 ] 15 minute cci( 26 ) >= 100 )
            )
        )
    )
)
"""