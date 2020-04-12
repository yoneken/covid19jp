import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def gen_eq_str(coefficients:list, x:str="x", y:str="y"):
    s = ""
    if len(coefficients) == 0:
        s += " 0"
    else:
        for i, coef in enumerate(coefficients):
            if i == len(coefficients) - 1:
                s += " {} {:.2f}".format("+" if coef>0 else "-", np.abs(coef))
            elif i == len(coefficients) - 2:
                s += " {} {:.2f} {}".format("+" if coef>0 else "-", np.abs(coef), x)
            else:
                s += " {} {:.2f} {}^{}".format("+" if coef>0 else "-", np.abs(coef), x, len(coefficients)-i-1)
    if s[1] == "+":
        s = s[2:]
    return "{} ={}".format(y, s)

def draw_approx_curve(x_data:np.ndarray, y_data:np.ndarray, r:range, 
    deg:int, forecast:int=14, color:str="green", info:str=""):
    x = [x_data[i] for i in r] - x_data[r.start]
    y = [y_data[i] for i in r] - y_data[r.start]
    coef = np.polyfit(x, y, deg)
    coef[deg] += y_data[r.start]
    x_f = [x_data[i] for i in range(r.start, r.stop + r.step * forecast, r.step)]
    curve = np.poly1d(coef)(x_f - x_data[r.start])
    label = gen_eq_str(coef)
    label = label[:label.rfind("x")+1]
    plt.plot(x_f, curve, c=color, label="{} {}".format(label, info))

def draw_approx_exp_curve(x_data:np.ndarray, y_data:np.ndarray, r:range, 
    forecast:int=14, color:str="green", info:str=""):
    x = [x_data[i] for i in r] - x_data[r.start]
    y = [y_data[i] for i in r] - y_data[r.start]

    def func(x, a, b, c):
        return a*np.exp(x/b)+c
    
    popt, pcov = curve_fit(func, x, y, p0=(500,5,0))
    x_f = [x_data[i] for i in range(r.start, r.stop + r.step * forecast, r.step)]
    curve = func((x_f - x_data[r.start]), popt[0], popt[1], popt[2]) + y_data[r.start]
    label = "y = {:.2f} e^(x/{:.2f}) ".format(popt[0], popt[1])
    plt.plot(x_f, curve, c=color, label="{} {}".format(label, info))

def main():
    df = pd.read_csv("COVID_2019.csv")

    j_confirmed = df.Japan.dropna().values[55:]
    #j_confirmed = df.USA.dropna().values[56:]
    xticks = df.date[55:]
    x_latent = np.array(range(len(xticks)))

    plt.scatter(x_latent[:len(j_confirmed)], j_confirmed, label="Observed")
    plt.xticks(x_latent, xticks, fontsize=7, rotation=70)

    #draw_approx_curve(x_latent, j_confirmed, range(26), 1, color="blue", info="(Fit for 1/21-2/15)")
    #draw_approx_curve(x_latent, j_confirmed, range(25,43), 1, info="(Fit for 2/15-3/4)")
    #draw_approx_curve(x_latent, j_confirmed, range(15), 2, color="orange", forecast=2, info="(Fit for 3/11-3/31)")
    #draw_approx_curve(x_latent, j_confirmed, range(43,64), 1, forecast=7, color="orange", info="(Fit for 3/4-3/26)")
    #draw_approx_curve(x_latent, j_confirmed, range(64,66), 1, forecast=7, color="purple", info="(Fit for 3/26-3/28)")
    #draw_approx_curve(x_latent, j_confirmed, range(67,69), 1, forecast=5, color="cyan", info="(Fit for 3/28-3/30)")
    #draw_approx_exp_curve(x_latent, j_confirmed, range(15), color="cyan", forecast=0, info="(Fit for 3/11-3/31)")
    #draw_approx_curve(x_latent, j_confirmed, range(15), 2, color="orange", forecast=2, info="(Fit for 3/11-3/31)")
    draw_approx_curve(x_latent, j_confirmed, range(9), 1, color="blue", info="(Fit for 3/16-3/25)")
    draw_approx_curve(x_latent, j_confirmed, range(9,11), 1, color="green", info="(Fit for 3/25-3/28)")
    #draw_approx_curve(x_latent, j_confirmed, range(9,21), 2, color="orange", forecast=10, info="(Fit for 3/25-4/6)")
    draw_approx_exp_curve(x_latent, j_confirmed, range(9,26), color="red", forecast=0, info="(Fit for 3/25-4/10)")

    plt.legend(fontsize=12)
    plt.title("Forecast of confirmed case of COVID-19 in Japan")
    #plt.title("Cumulative confirmed case of COVID-19 in USA")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()