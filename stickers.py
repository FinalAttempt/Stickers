#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy.integrate import quad
import numpy as np
import bigfloat
import argparse


class Stikers():
    """Calculate the amount paid for n stikers while exchanging with f friends
    n/f[*+]integrate_0^inf(1-(1-(1+x/2!+x**2)/e^x))dx
    Based on the video:
        The Math (and money) of Soccer Stickers - Numberphile
        (https://youtu.be/aKPkQCys86c)
    and:
       Soccer Stickers (extra math bit) - Numberphile
        (https://youtu.be/iMSitUaoS3I)"""

    def __init__(self, n, f, spp, valueperunit, valuetohigher, highersign, lastbuy):
        self.n = n
        self.f = f+1 #to be semanticly correct, one represents you, 2 is you and a friend
        self.spp = spp  # stickers per pack
        self.valueperunit = valueperunit
        self.valuetohigher = valuetohigher
        self.highersign = highersign
        self.lastbuy = lastbuy

    def lasum(self, x):
        return 1 + sum(bigfloat.pow(x, f) / bigfloat.factorial(f) for f in range(1, self.f))

    def calc_ExpectedToBuy(self, stop=0):
        return sum((self.n * 1.) / dec for dec in range(stop + 1, self.n + 1)[::-1])

    def integrand(self, x):
        return 1.0 - (1.0 - self.lasum(x)
                      / bigfloat.exp(x, bigfloat.precision(100)))**self.n

    def calc(self):
        try:
            a = quad(self.integrand, 0, np.inf)
            b = self.n / self.f * 1.
            title = "You and {} friend{}".format(self.f-1, "s" if self.f > 2 else "")
            print "\n=={}==".format("Alone" if self.f == 1 else title)
            print "Stickers you buy:\t{:.2f}\n" \
                  "         you pay:\t{}{:.2f}".format((b * a[0]), self.highersign,
                                                       ((b * a[0]) *
                                                        self.valueperunit)
                                                       / self.valuetohigher)
        except ZeroDivisionError:
            print("Cannot devide by zero.")

    def extrainfo(self):
        try:
            expected = self.calc_ExpectedToBuy()
            expectedWithBuy = self.calc_ExpectedToBuy(self.lastbuy)
            print "\n==Information=="
            print "To complete the album alone is expected " \
                  "you to buy {:.2f} stickers ({:.2f} packs)" \
                  ", paying {}{:.2f} for it.".format(expected, expected / self.spp,
                                                   self.highersign,
                                                   (expected *
                                                    self.valueperunit)
                                                   / self.valuetohigher)
            print "You will need to pay " \
                  "{}{:.2f} for {:.2f} stickers if you plan to buy the last " \
                  "{}{} directly " \
                  "from the company.".format(self.highersign,
                                             (expectedWithBuy *
                                              self.valueperunit)
                                             / self.valuetohigher,
                                             expectedWithBuy,
                                             self.lastbuy if self.lastbuy > 1 else "\b",
                                             " stickers" if self.lastbuy > 1 else " sticker")
            print "N=n*(log(n)+Euler constant) = " \
                  "{}".format(self.n * bigfloat.log(self.n) +
                              bigfloat.const_euler())
            print "---------------"
        except ZeroDivisionError:
            print("Cannot devide by zero.")


if __name__ == '__main__':
    print("=Stickers=")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', type=int, help='Number of stickers', required=True)
    parser.add_argument(
        '-f', type=int, help='Number of friends', required=True)
    parser.add_argument('-p', '--spp', type=int,
                        dest='spp', default=5, help='Number of stickers per pack')
    parser.add_argument('-u', '--unit', type=int,
                        dest='valueperunit', default=16, help='Value of a single unit, like penny')
    parser.add_argument('-b', '--basecurrency', default=100, type=int,
                        dest='valuetohigher', help='Ex: from pence to pounds')
    parser.add_argument('-s', '--sign', default='£', dest='highersign',
                        help='Currency sign')
    parser.add_argument('-l', '--lastbuy', type=int, default=50, dest='lastbuy',
                        help='How many stickers you can buy directly from the company')

    args = parser.parse_args()
    s = Stikers(**vars(args))
    s.extrainfo()
    s.calc()
