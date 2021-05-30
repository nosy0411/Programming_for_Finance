import QuantLib as ql
from draw_USbond_curve import GET_DATE, GET_QUOTE, TREASURY_CURVE

# Import Reference Curve Data
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
settlementDays = 1
faceValue = 100

fixedRateBond = ql.FixedRateBond(settlementDays, faceValue, schedule, couponRate, dayCount)

# Conduct Pricing
fixedRateBond.setPricingEngine(bondEngine)

# Calculate YTM
# 공시된 가격은 cleanprice 기준. 즉, clean price는 published value
targetPrice = fixedRateBond.cleanPrice()


# 좌변 채권가격을 target price(clean price 기준) 로 뒀을때 bondYield를 통해서 ytm을 구함
# 그 ytm을 InterestRate에 넣음. semiannual로 이산 방식으로 할인
ytm = ql.InterestRate(fixedRateBond.bondYield(targetPrice, dayCount, ql.Compounded, ql.Semiannual),
                        dayCount,
                        ql.Compounded,
                        ql.Semiannual)

print("Yield to Maturity = {:.4f}".format(ytm.rate()))

# calculate Duration & Convexity
print("Duration = {}".format(round(ql.BondFunctions.duration(fixedRateBond,ytm),4)))
print("Convexity = {}".format(round(ql.BondFunctions.convexity(fixedRateBond,ytm),4)))

