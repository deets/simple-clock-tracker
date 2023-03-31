import sys
import plotly.express as px
import pandas as pd
import numpy as np

from scipy.stats import exponnorm

df = pd.read_csv(sys.argv[1])

# This computes a fit to the skewed exponorm
# that seems to work well for the roundtrip
# UART communication I measured.
K, mu, sigma = exponnorm.fit(df["roundtrip"])
loc = mu
scale = sigma

# Rendering the distribution:
# import numpy as np
# from scipy.stats import exponnorm
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1, 1)


# K, mu, sigma = (0.6205714778937732, 0.0006558221748244949, 6.786911545123386e-05)

# loc = mu
# scale = sigma

# x = np.linspace(exponnorm.ppf(0.01, K, loc=loc, scale=scale),
#                 exponnorm.ppf(0.99, K, loc=loc, scale=scale), 100)
# ax.plot(x, exponnorm.pdf(x, K, loc=loc, scale=scale),
#        'r-', lw=5, alpha=0.6, label='exponnorm pdf')

# foo = exponnorm.rvs(K, loc=loc, scale=scale)
# breakpoint()
# plt.show()

x = np.linspace(exponnorm.ppf(0.01, K, loc=loc, scale=scale),
                exponnorm.ppf(0.99, K, loc=loc, scale=scale), 100)

foo = px.line(x, exponnorm.pdf(x, K, loc=loc, scale=scale))


fig = px.histogram(df, x="roundtrip")
#fig.add_trace(foo.data[0])
fig.show()
