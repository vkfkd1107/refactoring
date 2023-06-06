from __future__ import absolute_import

import math

from invoices import invoices as invoices_data
from plays import plays as plays_data


def statement(invoice, plays):
    totalAmount = 0
    volumeCredits = 0
    invoice_customer = invoice["customer"]
    result = f"청구 내역 (고객명: {invoice_customer})\n"

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        thisAmount = amountFor(perf, play)
        volumeCredits += max((perf["audience"] - 30), 0)

        if play["type"] == "comedy":
            volumeCredits += math.floor(perf["audience"] / 5)

        play_name = play["name"]
        perf_audience = perf["audience"]
        result += f"{play_name}: ${thisAmount/100:.2f} ({perf_audience}석)\n"
        totalAmount += thisAmount

    result += f"총액 ${totalAmount/100:.2f}\n"
    result += f"적립 포인트: ${volumeCredits}점\n"
    return result


def amountFor(perf, play):
    result = 0
    if play["type"] == "tragedy":
        result = 40000
        if perf["audience"] > 30:
            result += 1000 * (perf["audience"] - 30)
    elif play["type"] == "comedy":
        result = 30000
        if perf["audience"] > 20:
            result += 1000 + 500 * (perf["audience"] - 20)
        result += 300 * perf["audience"]
    else:
        raise Exception("알수없는 장르")
    return result


print(statement(invoices_data, plays_data))
