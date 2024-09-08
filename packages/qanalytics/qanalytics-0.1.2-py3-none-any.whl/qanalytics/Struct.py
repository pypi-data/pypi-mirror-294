from qanalytics.Enum import *

class DataSource:
    def __init__(self, pFile = '', pIsActivated = True):
        self.File = pFile
        self.IsActivated = pIsActivated
        self.Status = False
    def serialize(self):
        return {
            'File': self.File,
            'IsActivated': self.IsActivated,
            'Status': self.Status
        }
    def deserialize(self, pRoot):
        self.File = pRoot['File']
        self.IsActivated = pRoot['IsActivated']
        self.Status = pRoot['Status']
        return self

class Data:
    def __init__(self):
        self.Username = ''
        self.Password = ''
        self.Sources = []
        self.Attempts = 1
        self.SuccessOnRepoRequestFailure = False
        self.SuccessOnSpotRequestFailure = True
        self.SuccessOnFXSpotRequestFailure = False
        self.SuccessOnVolatilityRequestFailure = False
        self.SuccessOnYieldRequestFailure = True
        self.SuccessOnCorrelationRequestFailure = True
    def serialize(self):
        return {
            'Username': self.Username,
            'Password': self.Password,
            'Sources': [item.serialize() for item in self.Sources],
            'SuccessOnRepoRequestFailure': self.SuccessOnRepoRequestFailure,
            'SuccessOnSpotRequestFailure': self.SuccessOnSpotRequestFailure,
            'SuccessOnFXSpotRequestFailure': self.SuccessOnFXSpotRequestFailure,
            'SuccessOnVolatilityRequestFailure': self.SuccessOnVolatilityRequestFailure,
            'SuccessOnYieldRequestFailure': self.SuccessOnYieldRequestFailure,
            'SuccessOnCorrelationRequestFailure': self.SuccessOnCorrelationRequestFailure,
            'Attempts': self.Attempts
        }
    def deserialize(self, pRoot):
        self.Username = pRoot['Username']
        self.Password = pRoot['Password']
        self.Sources = [DataSource().deserialize(item) for item in pRoot['Sources']]
        self.Attempts = pRoot['Attempts']
        self.SuccessOnRepoRequestFailure = pRoot['SuccessOnRepoRequestFailure']
        self.SuccessOnSpotRequestFailure = pRoot['SuccessOnSpotRequestFailure']
        self.SuccessOnFXSpotRequestFailure = pRoot['SuccessOnFXSpotRequestFailure']
        self.SuccessOnVolatilityRequestFailure = pRoot['SuccessOnVolatilityRequestFailure']
        self.SuccessOnYieldRequestFailure = pRoot['SuccessOnYieldRequestFailure']
        self.SuccessOnCorrelationRequestFailure = pRoot['SuccessOnCorrelationRequestFailure']
        return self
    
class ICashFlow:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class Console(ICashFlow):
    def __init__(self):
        self.Script = ''
    def serialize(self):
        return {
            'Script': self.Script
        }
    def deserialize(self, pRoot):
        self.Script = pRoot['Script']
        return self
    
class File(ICashFlow):
    def __init__(self):
        self.File = ''
    def serialize(self):
        return {
            'File': self.File
        }
    def deserialize(self, pRoot):
        self.File = pRoot['File']
        return self
    
class Vanilla(ICashFlow):
    def __init__(self):
        self.Cliquet = []
    def serialize(self):
        return [item.serialize() for item in self.Cliquet]
    def deserialize(self, pRoot):
        self.Cliquet = []
        return self
    
class BasketItem:
    def __init__(self, Ticker = '', Weight = 0.0):
        self.Ticker = Ticker
        self.Weight = Weight
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Weight': self.Weight
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Weiht = pRoot['Weight']
        return self
    
class AutocallScheduleItem:
    def __init__(self,
        ObservationDate = '',
        PaymentDate = '',
        PaymentCurrency = '',
        Notional = 0.0,
        BarrierKind = '',
        AutocallBarrier = 0.0,
        AutocallBarrierSpreadLeft = 0.0,
        AutocallBarrierSpreadRight = 0.0,
        PhoenixCoupon = 0.0,
        CouponBarrier = 0.0,
        CouponBarrierSpreadLeft = 0.0,
        CouponBarrierSpreadRight = 0.0,
        BonusCoupon = 0.0
    ):
        self.ObservationDate = ObservationDate
        self.PaymentDate = PaymentDate
        self.PaymentCurrency = PaymentCurrency
        self.Notional = Notional
        self.BarrierKind = BarrierKind
        self.AutocallBarrier = AutocallBarrier
        self.AutocallBarrierSpreadLeft = AutocallBarrierSpreadLeft
        self.AutocallBarrierSpreadRight = AutocallBarrierSpreadRight
        self.PhoenixCoupon = PhoenixCoupon
        self.CouponBarrier = CouponBarrier
        self.CouponBarrierSpreadLeft = CouponBarrierSpreadLeft
        self.CouponBarrierSpreadRight = CouponBarrierSpreadRight
        self.BonusCoupon = BonusCoupon
    def serialize(self):
        return {
            'ObservationDate': self.ObservationDate,
            'PaymentDate': self.PaymentDate,
            'PaymentCurrency': self.PaymentCurrency,
            'Notional': self.Notional,
            'BarrierKind': self.BarrierKind,
            'AutocallBarrier': self.AutocallBarrier,
            'AutocallBarrierSpreadLeft': self.AutocallBarrierSpreadLeft,
            'AutocallBarrierSpreadRight': self.AutocallBarrierSpreadRight,
            'PhoenixCoupon': self.PhoenixCoupon,
            'CouponBarrier': self.CouponBarrier,
            'CouponBarrierSpreadLeft': self.CouponBarrierSpreadLeft,
            'CouponBarrierSpreadRight': self.CouponBarrierSpreadRight,
            'BonusCoupon': self.BonusCoupon
        }
    def deserialize(self, pRoot):
        self.ObservationDate = pRoot['ObservationDate']
        self.PaymentDate = pRoot['PaymentDate']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        self.Notional = pRoot['Notional']
        self.BarrierKind = pRoot['BarrierKind']
        self.AutocallBarrier = pRoot['AutocallBarrier']
        self.AutocallBarrierSpreadLeft = pRoot['AutocallBarrierSpreadLeft']
        self.AutocallBarrierSpreadRight = pRoot['AutocallBarrierSpreadRight']
        self.PhoenixCoupon = pRoot['PhoenixCoupon']
        self.CouponBarrier = pRoot['CouponBarrier']
        self.CouponBarrierSpreadLeft = pRoot['CouponBarrierSpreadLeft']
        self.CouponBarrierSpreadRight = pRoot['CouponBarrierSpreadRight']
        self.BonusCoupon = pRoot['BonusCoupon']
        return self
    
class Point:
    def __init__(self, X = 0.0, Y = 0.0):
        self.X = X
        self.Y = Y
    def serialize(self):
        return {
            'X': self.X,
            'Y': self.Y
        }
    def deserialize(self, pRoot):
        self.X = pRoot['X']
        self.Y = pRoot['Y']
        return self

class Autocall(ICashFlow):
    def __init__(self):
        self.Basket = []
        self.Schedule = []
        self.FinalPayment = []
        self.BonusCouponWithMemory = False
        self.BasketKind = BasketKind.BASKET
        self.StrikeKind = StrikeKind.ASIAN
        self.ForwardStartDate = ''
    def serialize(self):
        return {
            'Basket': [item.serialize() for item in self.Basket],
            'Schedule': [item.serialize() for item in self.Schedule],
            'FinalPayment': [item.serialize() for item in self.FinalPayment],
            'BonusCouponWithMemory': self.BonusCouponWithMemory,
            'BasketKind': self.BasketKind,
            'StrikeKind': self.StrikeKind,
            'ForwardStartDate': self.ForwardStartDate
        }
    def deserialize(self, pRoot):
        self.Basket = [BasketItem().deserialize(item) for item in pRoot['Basket']]
        self.Schedule = [AutocallScheduleItem().deserialize(item) for item in pRoot['Schedule']]
        self.FinalPayment = [Point().deserialize(item) for item in pRoot['FinalPayment']]
        self.BonusCouponWithMemory = pRoot['BonusCouponWithMemory']
        self.BasketKind = pRoot['BasketKind']
        self.StrikeKind = pRoot['StrikeKind']
        self.ForwardStartDate = pRoot['ForwardStartDate'] 
        return self

class Contract:
    def __init__(self):
        self.Date = ''
        self.Kind = ContractKind.CONSOLE
        self.CashFlow = None
        self.PremiumCurrency = ''
        self.IntradayFixings = False
        self.IntradayPayments = False
        self.IntradayChoices = False
    def serialize(self):
        root = self.CashFlow.serialize()
        root['Date'] = self.Date
        root['Kind'] = self.Kind.upper()
        root['PremiumCurrency'] = self.PremiumCurrency
        root['IntradayFixings'] = self.IntradayFixings
        root['IntradayPayments'] = self.IntradayPayments
        root['IntradayChoices'] = self.IntradayChoices
        return root
    def deserialize(self, pRoot):
        self.CashFlow.deserialize(pRoot)
        self.Date = pRoot['Date']
        self.PremiumCurrency = pRoot['PremiumCurrency']
        self.IntradayFixings = pRoot['IntradayFixings']
        self.IntradayPayments = pRoot['IntradayPayments']
        self.IntradayChoices = pRoot['IntradayChoices']
        return self

class Log:
    def __init__(self):
        self.Level = LogLevel.INFO
        self.Message = ''
    def serialize(self):
        return {
            'Level': self.Level,
            'Message': self.Message
        }
    def deserialize(self, pRoot):
        self.Level = pRoot['Level']
        self.Message = pRoot['Message']
        return self

class Logger:
    def __init__(self):
        self.Logs = []
    def serialize(self):
        return [item.serialize() for item in self.Logs]
    def deserialize(self, pRoot):
        self.Logs = [Log().deserialize(item) for item in pRoot]
        return self
    
class Underlying:
    def __init__(self):
        self.Ticker = ''
        self.CompleteName = ''
        self.QuoteCurrency = ''
        self.LastQuote = 0
        self.HasLastQuote = False
        self.AssetClass = AssetClass.DEPOSIT_RATE
        self.AssetKind = AssetKind.EQUITY
        self.IsQuanto = False
        self.IsInBasket = False
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'CompleteName': self.CompleteName,
            'LastQuote': self.LastQuote,
            'HasLastQuote': self.HasLastQuote,
            'AssetClass': self.AssetClass,
            'AssetKind': self.AssetKind,
            'IsQuanto': self.IsQuanto,
            'IsInBasket': self.IsInBasket
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.CompleteName = pRoot['CompleteName']
        self.LastQuote = pRoot['LastQuote']
        self.HasLastQuote = pRoot['HasLastQuote']
        self.AssetClass = pRoot['AssetClass']
        self.AssetKind = pRoot['AssetKind']
        self.IsQuanto = pRoot['IsQuanto']
        self.IsInBasket = pRoot['IsInBasket']
        return self

class Fixing:
    def __init__(self):
        self.Date = ''
        self.QuoteCurrency = ''
        self.Ticker = ''
        self.Quote = 0
        self.HasQuote = False
        self.IsPast = False
        self.Edit = False
    def serialize(self):
        return {
            'Date': self.Date,
            'QuoteCurrency': self.QuoteCurrency,
            'Ticker': self.Ticker,
            'Quote': self.Quote,
            'HasQuote': self.HasQuote,
            'IsPast': self.IsPast,
            'Edit': self.Edit
        }
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.QuoteCurrency = pRoot['QuoteCurrency']
        self.Ticker = pRoot['Ticker']
        self.Quote = pRoot['Quote']
        self.HasQuote = pRoot['HasQuote']
        self.IsPast = pRoot['IsPast']
        self.Edit = pRoot['Edit']
        return self

class Correlation:
    def __init__(self):
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self

class CorrelationMatrix:
    def __init__(self):
        self.Rows = []
        self.Cols = []
        self.Data = [[]]
    def serialize(self):
        return {
            'Rows': self.Rows,
            'Cols': self.Cols,
            'Data': self.Data
        }
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = pRoot['Data']
        return self

class IEvent:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class PaymentEvent(IEvent):
    def __init__(self):
        self.Currency = ''
        self.Script = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Currency': self.Currency,
            'Script': self.Script,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Currency = pRoot['Currency']
        self.Script = pRoot['Script']
        self.HasValue = pRoot['HasValue']
        return self
    
class PurchaseEvent(IEvent):
    def __init__(self):
        self.Quantity = 0
        self.Start = 0
        self.End = 0
    def serialize(self):
        return {
            'Quantity': self.Quantity,
            'Start': self.Start,
            'End': self.End
        }
    def deserialize(self, pRoot):
        self.Quantity = pRoot['Quantity']
        self.Start = pRoot['Start']
        self.End = pRoot['End']
        return self
    
class FixingEvent(IEvent):
    def __init__(self):
        self.Ticker = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Value': self.Value,
            'HasValue': self.HasValued
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class SettingEvent(IEvent):
    def __init__(self):
        self.Name = ''
        self.Script = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Name': self.Name,
            'Script': self.Script,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Script = pRoot['Script']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class ChoiceEvent(IEvent):
    def __init__(self):
        self.ChoiceOwnership = ''
        self.Starts = []
        self.Ends = []
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'ChoiceOwnership': self.ChoiceOwnership,
            'Starts': self.Starts,
            'Ends': self.Ends,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.ChoiceOwnership = pRoot['ChoiceOwnership']
        self.Starts = pRoot['Starts']
        self.Ends = pRoot['Ends']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class BarrierEvent(IEvent):
    def __init__(self):
        self.WithSpread = False
        self.SpreadLeft = 0
        self.SpreadRight = 0
        self.Script = ''
        self.StartLeft = 0
        self.StartRight = 0
        self.EndLeft = 0
        self.EndRight = 0
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'WithSpread': self.WithSpread,
            'SpreadLeft': self.SpreadLeft,
            'SpreadRight': self.SpreadRight,
            'Script': self.Script,
            'StartLeft': self.StartLeft,
            'StartRight': self.StartRight,
            'EndLeft': self.EndLeft,
            'EndRight': self.EndRight,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.WithSpread = pRoot['WithSpread']
        self.SpreadLeft = pRoot['SpreadLeft']
        self.SpreadRight = pRoot['SpreadRight']
        self.Script = pRoot['Script']
        self.StartLeft = pRoot['StartLeft']
        self.StartRight = pRoot['StartRight']
        self.EndLeft = pRoot['EndLeft']
        self.EndRight = pRoot['EndRight']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self

class EndEvent(IEvent):
    def serialize(self):
        return None
    def deserialize(self, _):
        return self
    
class Event:
    def __init__(self):
        self.EventKind = EventKind.BARRIER
        self.Date = ''
        self.Attributes = None
    def serialize(self):
        return {
            'EventKind': self.EventKind,
            'Date': self.Date,
            'Attributes': self.Attributes.serialize()
        }
    def deserialize(self, pRoot):
        self.EventKind = pRoot['EventKind']
        self.Date = pRoot['Date']
        self.Attributes.deserialize(pRoot['Attributes'])
        return self
    
class ContractResults:
    def __init__(self):
        # Input.
        self.RequestScript = True
        self.RequestUnderlyings = True
        self.RequestFixings = True
        self.RequestCorrelations = True
        self.RequestEvents = True

        # Output.
        self.Script = ''
        self.IndentSize = 0
        self.Underlyings = []
        self.Fixings = []
        self.CorrelationMatrix = CorrelationMatrix()
        self.Events = []
    def serialize(self):
        return {
            'RequestScript': self.RequestScript,
            'RequestUnderlyings': self.RequestUnderlyings,
            'RequestFixings': self.RequestFixings,
            'RequestCorrelations': self.RequestCorrelations,
            'RequestEvents': self.RequestEvents,
            'Script': self.Script,
            'IndentSize': self.IndentSize,
            'Underlyings': self.Underlyings,
            'Fixings': self.Fixings,
            'CorrelationMatrix': self.CorrelationMatrix.serialize(),
            'Events': self.Events
        }
    def deserialize(self, pRoot):
        self.RequestScript = pRoot['RequestScript']
        self.RequestUnderlyings = pRoot['RequestUnderlyings']
        self.RequestFixings = pRoot['RequestFixings']
        self.RequestCorrelations = pRoot['RequestCorrelations']
        self.RequestEvents = pRoot['RequestEvents']
        self.Script = pRoot['Script']
        self.IndentSize = pRoot['IndentSize']
        self.Underlyings = [Underlying().deserialize(item) for item in pRoot['Underlyings']]
        self.Fixings = [Fixing().deserialize(item) for item in pRoot['Fixings']]
        self.CorrelationMatrix.deserialize(pRoot['CorrelationMatrix'])
        self.Events = pRoot['Events']
        return self
    