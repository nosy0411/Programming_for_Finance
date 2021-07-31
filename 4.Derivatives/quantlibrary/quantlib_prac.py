import QuantLib as ql  # Construction

date1 = ql.Date(11, 4, 2020)
date2 = ql.Date(43932)
print(date1)
print(date2)

# Basic Functions
date = ql.Date(11, 4, 2020)
dayOfMonth = date.dayOfMonth()
dayOfYear = date.dayOfYear()
month = date.month()
year = date.year()
serialNumber = date.serialNumber()
weekday = date.weekday()

print("Day of Month = {}".format(dayOfMonth))
print("Day of Year = {}".format(dayOfYear))
print("Month = {}".format(month))
print("Year = {}".format(year))
print("Serial Number = {}".format(serialNumber))
print("Weekday = {}".format(weekday))
print('\n')
# Advanced Functions 
date = ql.Date(12, 4, 2020) 
todaysDate = date.todaysDate() 
isLeap = date.isLeap(date.year()) 
isEndOfMonth = date.isEndOfMonth(date) 
endOfMonth = date.endOfMonth(date) 
nextWeekday = date.nextWeekday(date, 4) 
nthWeekday = date.nthWeekday(3, 5, 7, 2020) 

print("Today's Date = {}".format(todaysDate)) 
print("is Leap? = {}".format(isLeap)) 
print("is End of Month? = {}".format(isEndOfMonth)) 
print("End of Month = {}".format(endOfMonth)) 
print("Next Weekday = {}".format(nextWeekday)) 
print("Nth Weekday = {}".format(nthWeekday))
print('\n')

import QuantLib as ql # Construction 

period1 = ql.Period(3, ql.Months) 
period2 = ql.Period(ql.Semiannual)

# Functions 
date1 = ql.Date(11, 4, 2020) 
date2 = ql.Date(31, 12, 2020) 
three_weeks = ql.Period(3, ql.Weeks) 
three_months = ql.Period(3, ql.Months) 
three_years = ql.Period(3, ql.Years) 

print("After 3 Weeks : {}".format(date1 + three_weeks)) 
print("After 3 Months : {}".format(date1 + three_months)) 
print("After 3 Years : {}".format(date1 + three_years)) 
print("Days between Date2 and Date1 = {}".format(date2 - date1))
print('\n')

import QuantLib as ql # Construction 

us = ql.UnitedStates() 
eu = ql.TARGET() 
kr = ql.SouthKorea() 
jp = ql.Japan() 
cn = ql.China() 

date1 = ql.Date(1, 1, 2020) 
date2 = ql.Date(31, 12, 2020) 

kr_holidayList = kr.holidayList(kr, date1, date2) 
print(kr_holidayList)
print('\n')

kr.addHoliday(ql.Date(27, 1, 2020)) 
kr.addHoliday(ql.Date(15, 4, 2020)) 
kr.removeHoliday(ql.Date(6, 5, 2020)) 
print(kr_holidayList)
print('\n')

kr.businessDaysBetween(date1, date2) #249
kr.isBusinessDay(date1) # False 
kr.isHoliday(date1) # True

kr.advance(date1, ql.Period(6, ql.Months), ql.ModifiedFollowing, True) # July 1st, 2020

new_calendar = ql.JointCalendar(us, eu, kr)
print(new_calendar.holidayList(new_calendar, date1, date2))
print('\n')

import QuantLib as ql # Construction 
act360 = ql.Actual360() # Actual/360 
act365 = ql.Actual365Fixed() # Actual/365 
actact = ql.ActualActual() # Actual/Actual 
thirty360 = ql.Thirty360() # 30/360 
b252 = ql.Business252() # BusinessDay/252

date1 = ql.Date(12, 2, 2020) 
date2 = ql.Date(14, 5, 2020) # Day Count 
print("Day Count by Actual/360 = {}".format(act360.dayCount(date1, date2))) 
print("Day Count by Actual/365 = {}".format(act365.dayCount(date1, date2))) 
print("Day Count by Actual/Actual = {}".format(actact.dayCount(date1, date2))) 
print("Day Count by 30/360 = {}".format(thirty360.dayCount(date1, date2))) 
print("Day Count by BusinessDay/252 = {}".format(b252.dayCount(date1, date2)))
print('\n')

# Year Fraction 
print("Year Fraction by Actual/360 = {}".format(round(act360.yearFraction(date1, date2), 4))) 
print("Year Fraction by Actual/365 = {}".format(round(act365.yearFraction(date1, date2), 4))) 
print("Year Fraction by Actual/Actual = {}".format(round(actact.yearFraction(date1, date2), 4))) 
print("Year Fraction by 30/360 = {}".format(round(thirty360.yearFraction(date1, date2), 4))) 
print("Year Fraction by BusinessDay/252 = {}".format(round(b252.yearFraction(date1, date2), 4)))
print('\n')

import QuantLib as ql 

# Components 
effectiveDate = ql.Date(13, 4, 2020) 
maturityDate = ql.Date(15, 4, 2023) 
tenor = ql.Period(3, ql.Months) 
calendar = ql.SouthKorea() 
convention = ql.ModifiedFollowing 
rule = ql.DateGeneration.Backward 
endOfMonth = False 

# Construction 
schedule = ql.Schedule(effectiveDate, maturityDate, tenor, calendar, convention, convention, rule, endOfMonth)
ref_date = ql.Date(4, 10, 2021) # Functions 
print("Next Payment Date from {} : {}".format(ref_date, schedule.nextDate(ref_date))) 
print("Previous Payment Date from {} : {}".format(ref_date, schedule.previousDate(ref_date)))
print('\n')

import QuantLib as ql 
# Construction 
quote = ql.SimpleQuote(2767.88)
# Functions 
print(quote.value()) # 2767.88 
quote.setValue(2800.0) 
print(quote.value()) # 2800.0

import QuantLib as ql 
# Components 
rate = 0.0148 
dc = ql.ActualActual() 
comp = ql.Compounded 
freq = ql.Annual 

# Construction 
ir = ql.InterestRate(rate, dc, comp, freq)

# Discount & Compound Factor 
start_date = ql.Date(19, 4, 2020) 
end_date = ql.Date(19, 4, 2021) 
print("Discount Factor between {} and {} = {}".format(start_date, end_date, round(ir.discountFactor(t), 4))) 
print("Compounding Factor between {} and {} = {}".format(start_date, end_date, round(ir.compoundFactor(t), 4)))

# Equivalent Rate 
new_dc = ql.ActualActual() 
new_comp = ql.Compounded 
new_freq = ql.Quarterly 
print("Equivalent Rate = {}".format(ir.equivalentRate(new_dc, new_comp, new_freq, start_date, end_date)))

# Implied Rate 
comp_factor = 1.05 
new_dc = ql.ActualActual() 
new_comp = ql.Compounded 
new_freq = ql.Annual 
print("Implied Rate = {}".format(ir.impliedRate(comp_factor, new_dc, new_comp, new_freq, start_date, end_date)))

import QuantLib as ql # Components 
name = "USD_3M_Libor" 
tenor = ql.Period(ql.Quarterly) 
settlementDays = 2 
currency = ql.USDCurrency() 
calendar = ql.UnitedStates() 
convention = ql.ModifiedFollowing 
endOfMonth = False 
dayCounter = ql.Actual360() 

# Construction 
usd_3m_libor = ql.IborIndex(name, tenor, settlementDays, currency, calendar, convention, endOfMonth, dayCounter)
usd_3m_libor.addFixing(ql.Date(27, 4, 2020), 0.0135) 
usd_3m_libor.clearFixings()