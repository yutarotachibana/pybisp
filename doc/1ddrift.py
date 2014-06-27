# Estimating approximate likelihood inference for the parameters of the one dimensional drift-diffusion process:
# This work is under progress:
#
{
 "metadata": {
  "name": "drift"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "code",
     "collapsed": false,
     "input": "import numpy as np\nimport matplotlib as mpl\nimport matplotlib.pyplot as plt\nimport pylab as pl\nfrom __future__ import division",
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 9
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": "##The one dimensional drift-diffusion process and its transition probability density\nThe one dimensional drift-diffusion process is described by the following stochastic differential equation:\n$dx = adt + \\sqrt{2Dt}dW$ for which the Fokker-Planck equation is $\\frac{\\partial P}{\\partial t}  = D \\frac{\\partial^{2}P}{\\partial x^{2}}\n-a\\frac{\\partial P}{\\partial x}$. a is a drift and W is a wiener process which models white noise. The transition probability density is\ngiven by $P(x,t) = \\frac{1}{\\sqrt{2\\pi Dt}}\\exp{-\\frac{(x-at)^{2}}{2Dt}}$. The exact solution is the Gaussian with mean and variance given\nby $\\langle x(t)\\rangle = \\int\\limits_{-\\infty}^\\infty x p(x,t)dx$ = at, $\\langle x^{2} \\rangle - \\langle x \\rangle ^2$ = Dt so that the\ntransition probability density is given by $P(x,t) = \\frac{1}{\\sqrt{2\\pi Dt}}\\exp{-\\frac{(x-at)^{2}}{2Dt}}$.\nThe parameters are $a = \\frac{\\langle x(t)\\rangle}{t}$, $ D = \\frac{\\langle x^{2} \\rangle - \\langle x \\rangle ^2}{t}$. The parameter in this \nprocess is  D and a.\n"
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": "##Inference problem:\nThe inference problem for D can be stated as  follows: For the given discrete smapled path, the probability density for D using Bayes theorem\ncan be written as follows:$$ P(D| x_1, x_2, \\ldots x_N)  = \\frac{\\Pi_{i=1}^N P(x_i | x_{i-1}, D)P(D)}{\\int dD \\Pi_{i=1}^N P(x_i | x_{i-1},\n D)P(D)}$$. P(D) is the prior distribution which we can take as $\\frac{1}{D}$, the Jeffrey prior. The logarithm of the probability distribution\n is, $$ \\log P(D) = \\frac{-(N+1)}{2}+\\frac{\\delta^{2}}{2D\\delta t}$$ where $\\delta^{2} = ((x{i}-x_{i-1})- a t_{i} )^{2}$\n    \n    \n    \n    \n    \n    \n\n    \n    "
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": "def logprob(D, dx2, dt, N):\n    return -dx2/(2*D*dt) - np.log(D) -0.5*(N-1)*np.log(2*D*np.pi*(dt))\n            \nN = 1500\nt = arange(N)                  # sampling times\ndw = np.random.randn(N)        # Wiener increments\nx = np.cumsum(dw)\na = 0.5\n\ndx2 = sum((x[1:] - x[:-1]-a*t[0])**2)\ndt = t[1] - t[0]\n\n\nD = np.linspace(0.8,1.2, 1028)\n#D = np.linspace(0.8,1.2, 1024)\n\n\nplot(D, logprob(D, dx2, dt, N),'-',lw=1)\n\n\nxlabel('D')\nylabel('P(D)')\ngrid('on')\n\nprint dx2/(N*dt)",
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": "1.00355281084\n"
      },
      {
       "output_type": "display_data",
       "png": "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\nfypQS1xEtIqwAAAAAElFTkSuQmCC\n"
      }
     ],
     "prompt_number": 10
    }
   ],
   "metadata": {}
  }
 ]
}
