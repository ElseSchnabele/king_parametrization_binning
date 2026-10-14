import matplotlib.pyplot as plt
import histlite as hl
import pandas as pd
import numpy as np

def plot_bias(king_allt, rayleigh_allt, ns_bins, expect_gamma, fitting_candidate_sindec = None):


    fig, axs = plt.subplots(
        2, 2,
        figsize=(7, 5),
        sharex="col",
        gridspec_kw={"height_ratios": [3, 1]},
    )

    # ---------- n_s plot ----------
    ax = axs[0, 0]
    rax = axs[1, 0]

    h_king = hl.hist(
        (king_allt["ntrue"], king_allt["ns"]),
        bins=(ns_bins, 100),
    ).contain_project(1)

    h_ray = hl.hist(
        (rayleigh_allt["ntrue"], rayleigh_allt["ns"]),
        bins=(ns_bins, 100),
    ).contain_project(1)

    hl.plot1d(ax, h_king, errorbands=True, drawstyle="default", label="King")
    hl.plot1d(ax, h_ray, errorbands=True, drawstyle="default", label="Rayleigh")

    x_ns = h_king.centers[0]

    # deviation from expectation: n_s = n_inj
    king_dev = h_king.values - x_ns
    ray_dev  = h_ray.values - x_ns

    # mean absolute deviation
    king_mean_dev_sig = np.mean(np.abs(king_dev))
    ray_mean_dev_sig  = np.mean(np.abs(ray_dev))

    rax.axhline(0, color="k", lw=1)
    rax.plot(
        x_ns,
        king_dev,
        drawstyle="steps-mid",
        label=f"King ⟨Δ⟩={king_mean_dev_sig:.2f}",
    )
    rax.plot(
        x_ns,
        ray_dev,
        drawstyle="steps-mid",
        label=f"Rayleigh ⟨Δ⟩={ray_mean_dev_sig:.2f}",
    )

    lim = ns_bins[[0, -1]]
    ax.plot(lim, lim, color="grey", ls="--", lw=1, zorder=-10)

    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_aspect("equal")

    ax.set_ylabel(r"$n_s$")
    rax.set_ylabel(r"$n_s - n_\mathrm{inj}$")
    rax.set_xlabel(r"$n_\text{inj}$")

    # ---------- gamma plot ----------
    ax = axs[0, 1]
    rax = axs[1, 1]

    h_king = hl.hist(
        (king_allt["ntrue"], king_allt["gamma"]),
        bins=(ns_bins, 100),
    ).contain_project(1)

    h_ray = hl.hist(
        (rayleigh_allt["ntrue"], rayleigh_allt["gamma"]),
        bins=(ns_bins, 100),
    ).contain_project(1)

    hl.plot1d(ax, h_king, errorbands=True, drawstyle="default", label="King")
    hl.plot1d(ax, h_ray, errorbands=True, drawstyle="default", label="Rayleigh")

    x_gamma = h_king.centers[0]

    # reference line: gamma = expect_gamma
    gamma_ref = expect_gamma

    king_dev = h_king.values - gamma_ref
    ray_dev  = h_ray.values - gamma_ref

    # mean deviation
    king_mean_dev_gamma = np.mean(np.abs(king_dev))
    ray_mean_dev_gamma  = np.mean(np.abs(ray_dev))

    rax.axhline(0, color="k", lw=1)
    rax.plot(
        x_gamma,
        king_dev,
        drawstyle="steps-mid",
        label=f"King ⟨Δ⟩={king_mean_dev_gamma:.2f}",
    )
    rax.plot(
        x_gamma,
        ray_dev,
        drawstyle="steps-mid",
        label=f"Rayleigh ⟨Δ⟩={ray_mean_dev_gamma:.2f}",
    )

    ax.axhline(gamma_ref, color="grey", ls="--", lw=1, zorder=-10)
    ax.set_xlim(axs[0, 0].get_xlim())

    ax.set_ylabel(r"$\gamma$")
    rax.set_ylabel(r"$\gamma - \gamma_\mathrm{exp}$")
    rax.set_xlabel(r"$n_\text{inj}$")

    for ax in axs.flat:
        ax.grid()

    axs[0, 0].legend()
    axs[1, 0].legend()
    axs[1, 1].legend()
    if fitting_candidate_sindec is not None:
        fig.suptitle(f"Sin($\delta$) = {fitting_candidate_sindec}")
    fig.tight_layout()
    plt.show()
    
    return {
        'king_mean_dev_sig' : king_mean_dev_sig,
        'rayleigh_mean_dev_sig' : ray_mean_dev_sig,
        'king_mean_dev_gamma' : king_mean_dev_gamma,
        'rayleigh_mean_dev_gamma' : ray_mean_dev_gamma,
    }
    

def plot_flux(king_data, rayleigh_data, folder_name, sky : str, show_title = True, x_lim = (-0.85, 0.85), figsize = (10, 6)):
        
    sin_decs = sorted(list(king_data[sky][folder_name].keys()))
    y = []
    yerr = []
    rayleigh_y = []
    rayleigh_yerr = []
    filtered_sin_decs = []
    

    for k in sin_decs:
        king_d = king_data[sky][folder_name][k]
        rayleigh_d = rayleigh_data[k]

        flux = king_d["flux"]
        flux_err = king_d["flux_err"]

        # skip invalid King points
        try:
            flux = float(king_d["flux"])
            flux_err = float(king_d["flux_err"])
        except (TypeError, ValueError):
            continue

        if not (np.isfinite(flux) and np.isfinite(flux_err)):
            continue

        y.append(flux)
        yerr.append(flux_err)

        rayleigh_y.append(rayleigh_d["flux"])
        rayleigh_yerr.append(rayleigh_d["flux_err"])
        # keep x in sync with the filtered arrays
        filtered_sin_decs.append(k)
    x = np.asarray(filtered_sin_decs)
    y = np.asarray(y)
    yerr = np.asarray(yerr)

    rayleigh_y = np.asarray(rayleigh_y)
    rayleigh_yerr = np.asarray(rayleigh_yerr)

    # total score metric
    llh_score = np.mean(y / rayleigh_y)


    ratio = y / rayleigh_y

    ratio_err = ratio * np.sqrt(
        (yerr / y)**2 +
        (rayleigh_yerr / rayleigh_y)**2
    )
    # --- plotting ---
    fig, (ax, ax_diff) = plt.subplots(
        2,
        1,
        figsize=figsize,
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1], "hspace": 0.05},
    )
    if show_title:
        ax.set_title(folder_name + r", $\overline{r}_s =$" + str(llh_score.round(4)))

    # top panel
    ax.set_yscale("log")

    ax.axvspan(-0.17, -0.03, color="grey", alpha=0.2, zorder=2)

    ax.errorbar(
        x,
        y,
        yerr=yerr,
        ls="dotted",
        marker="s",
        capsize=3,
        markersize = 3,
        zorder=3,
        label=r"King",
    )

    ax.errorbar(
        x,
        rayleigh_y,
        yerr=rayleigh_yerr,
        ls="dotted",
        marker="s",
        capsize=3,
        zorder=2,
        markersize = 3,
        label=r"Rayleigh",
    )

    ax.legend()
    ax.set_xlim(x_lim)
    ax.set_ylabel(r"$E^2 dN/dE$ [TeV cm$^{-2}$ s$^{-1}$] @ 100 TeV")
    ax.grid(which="both", zorder=1)

    # bottom panel
    ax_diff.axhline(1, color="black", lw=1, ls="--")
    ax_diff.axvspan(-0.17, -0.03, color="grey", alpha=0.2, zorder=2)

    ax_diff.errorbar(
        x,
        ratio,
        yerr=ratio_err,
        ls="dotted",
        capsize=3,
        marker = 's',
        markersize = 3,
        zorder=3,
        color="black",
    )

    ax_diff.set_xlabel(r"$\sin{(\mathrm{dec})}$")
    ax_diff.set_ylabel(r"$\Phi_{\rm King}/\Phi_{\rm Rayleigh}$")
    ax_diff.legend()
    ax_diff.grid(which="both", zorder=1)
    plt.show()
    return {'avg_ratio' : llh_score,
            'ratio' : ratio,
            'king_flux' : y,
            'rayleigh_flux' : rayleigh_y}
    
    
def box_plot_binning_configs(summary_df: pd.DataFrame, metric: str, sin_decs: list, ylim = list):
    data = [summary_df[summary_df['sin_dec'] == k][metric] for k in sin_decs]

    plt.figure(figsize = (8, 4))
    plt.axhline(1, color="black", lw=1, ls="--")
    plt.axhspan(1, ylim[1], color = 'red', alpha = 0.1)
    plt.axhspan(ylim[0], 1, color = 'lime', alpha = 0.1)
    plt.boxplot(
        data,
        positions=sin_decs,   # x-positions of the boxes
        widths=0.02,             # adjust to your spacing
        showfliers=False,        # optional
        manage_ticks=False,
    )
    plt.ylim(ylim)
    plt.xlabel(r"$\sin{(\mathrm{dec})}$")
    plt.ylabel(r"$\Phi_{\rm King}/\Phi_{\rm Rayleigh}$")
    plt.grid(which="both", zorder=1)