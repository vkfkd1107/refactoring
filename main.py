from __future__ import absolute_import

import math

from invoices import invoices as invoices_data
from plays import plays as plays_data


def statement(invoice, plays):
    totalAmount = 0
    invoice_customer = invoice["customer"]
    result = f"청구 내역 (고객명: {invoice_customer})\n"

    def playFor(aPerformance):
        return plays[aPerformance["playID"]]

    def amountFor(aPerformance):
        result = 0
        if playFor(perf)["type"] == "tragedy":
            result = 40000
            if aPerformance["audience"] > 30:
                result += 1000 * (aPerformance["audience"] - 30)
        elif playFor(perf)["type"] == "comedy":
            result = 30000
            if aPerformance["audience"] > 20:
                result += 1000 + 500 * (aPerformance["audience"] - 20)
            result += 300 * aPerformance["audience"]
        else:
            raise Exception("알수없는 장르")
        return result

    def volumeCreditsFor(perf):
        result = 0
        result += max((perf["audience"] - 30), 0)
        if playFor(perf)["type"] == "comedy":
            result += math.floor(perf["audience"] / 5)
        return result

    def totalVolumeCredits():
        result = 0
        for perf in invoice["performances"]:
            result += volumeCreditsFor(perf)
        return result

    def totalAmount():
        result = 0
        for perf in invoice["performances"]:
            result += amountFor(perf)
        return result

    for perf in invoice["performances"]:
        play_name = playFor(perf)["name"]
        perf_audience = perf["audience"]
        result += f"{play_name}: ${amountFor(perf)/100:.2f} ({perf_audience}석)\n"

    result += f"총액 ${totalAmount()/100:.2f}\n"
    result += f"적립 포인트: ${totalVolumeCredits()}점\n"
    return result


print(statement(invoices_data, plays_data))
