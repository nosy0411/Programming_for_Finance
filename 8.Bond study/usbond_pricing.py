import QuantLib as ql
from draw_USbond_curve import GET_DATE, GET_QUOTE, TREASURY_CURVE

ref_date=GET_DATE()
quote=GET_QUOTE(ref_date)
curve=TREASURY_CURVE(ref_date,quote)

# Convert into Engine

spotCurveHandle = ql.YieldTermStructureHandle(curve)
bondEngine = ql.DiscountingBondEngine(spotCurveHandle)

# Treasury Bond Specifiation
issueDate = ql.Date(15,11,2019)
maturityDate = ql.Date(15,11,2029)
coupon_frequency = ql.Period(ql.Semiannual)
calendar = ql.UnitedStates()
convention = ql.ModifiedFollowing
dateGeneration = ql.DateGeneration.Backward
monthEnd = False

schedule = ql.Schedule(issueDate,
                        maturityDate,
                        coupon_frequency,
                        calendar,
                        convention,
                        convention,
                        dateGeneration,
                        monthEnd)

dayCount = ql.ActualActual()
couponRate = [0.0175]

# settlementDays 돈을 받는 날짜  --today --(fixingdays)--spot date --- settlement date 
settlementDays = 1
faceValue = 100

fixedRateBond = ql.FixedRateBond(settlementDays, faceValue, schedule, couponRate, dayCount)

# Conduct Pricing
fixedRateBond.setPricingEngine(bondEngine)

# Result
print("Bond Price = {}".format(round(fixedRateBond.NPV(),4)))

for c in fixedRateBond.cashflows():
    print('%20s %12f' % (c.date(), c.amount()))


