from __future__ import annotations

from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.patches import Rectangle, FancyArrowPatch

# =============================================================================
# Paths
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # scripts/ -> project root
ASSETS_DIR = PROJECT_ROOT / "assets"
RUN_SLUG = "woodcorp-otif-rootcause"  # <- adjust if needed

OUT_DIR = ASSETS_DIR / RUN_SLUG
PLOTS_DIR = OUT_DIR / "plots"
TABLES_DIR = OUT_DIR / "tables"
FLAGS_DIR = OUT_DIR / "flags"

for d in [PLOTS_DIR, TABLES_DIR, FLAGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CSV_PATH = PROJECT_ROOT / r"data\8c) Woodcorp O2C Case table.csv"

TOP_N = 15
MIN_CASES = 200

# =============================================================================
# Slide-matching palette
# =============================================================================
PAL = {
    "teal": "#214D49",      # primary
    "mint": "#84A7A2",      # secondary
    "gold": "#D4B059",      # highlight
    "text": "#222326",
    "grid": "#DDE1E1",
    "mid_grey": "#5F6665",
    "bg": "#FFFFFF",
}

# =============================================================================
# Global style (matplotlib best practice for reports)
# =============================================================================
def apply_slide_style() -> None:
    plt.rcParams.update({
        "figure.facecolor": PAL["bg"],
        "axes.facecolor": PAL["bg"],
        "savefig.facecolor": PAL["bg"],
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.edgecolor": PAL["grid"],
        "axes.linewidth": 1.0,
        "axes.labelcolor": PAL["text"],
        "text.color": PAL["text"],
        "xtick.color": PAL["mid_grey"],
        "ytick.color": PAL["mid_grey"],
        "grid.color": PAL["grid"],
        "grid.linestyle": "-",
        "grid.linewidth": 0.8,
        "legend.frameon": False,
    })

apply_slide_style()

# =============================================================================
# Helpers
# =============================================================================
def try_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path.resolve()}")
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(path, sep=sep, dtype=str, engine="python")
            if df.shape[1] > 3:
                return df
        except Exception:
            pass
    raise ValueError("Could not read CSV robustly (check delimiter/format).")

def parse_eu_number(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.number)):
        return float(x)
    s = str(x).strip().strip('"').replace(" ", "")
    if s == "":
        return np.nan
    # 1.234,56 -> 1234.56 ; 123,45 -> 123.45
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan

def savefig(name: str) -> Path:
    p = PLOTS_DIR / name
    plt.tight_layout()
    plt.savefig(p, dpi=220, bbox_inches="tight")
    plt.close()
    return p

def fmt_int(x) -> str:
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return "0"

def pct(x, _pos=None):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return f"{x*100:.0f}%"

PCT_FMT = FuncFormatter(pct)

def set_axis_from_zero(ax, which: str, data: np.ndarray, pad: float = 0.06) -> None:
    """
    Force scale to start at 0 (management convention).
    Adds small upper padding for readability.
    """
    data = np.asarray(data, dtype=float)
    data = data[np.isfinite(data)]
    if data.size == 0:
        lo, hi = 0.0, 1.0
    else:
        lo, hi = 0.0, float(np.max(data))
        if hi <= 0:
            hi = 1.0
    hi = hi * (1.0 + pad)
    if which.lower() == "x":
        ax.set_xlim(lo, hi)
    elif which.lower() == "y":
        ax.set_ylim(lo, hi)

def style_axes(ax) -> None:
    ax.grid(True, axis="both", alpha=0.9)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(PAL["grid"])
    ax.spines["bottom"].set_color(PAL["grid"])
    ax.tick_params(axis="both", which="major", length=4, width=1)

# =============================================================================
# KPI Engineering
# =============================================================================
def engineer_kpis(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = [
        "ORDERED_QUANTITY", "DELIVERED_QUANTITY",
        "MIN_ORDER_TOLERANCE", "MAX_ORDER_TOLERANCE",
        "ORDER_VALUE", "UNIT_PRICE",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].apply(parse_eu_number), errors="coerce")

    for c in ["DELIVERED_DATE", "PROMISED_DATE"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    tmin = df.get("MIN_ORDER_TOLERANCE", pd.Series(np.nan, index=df.index)).fillna(0.0)
    tmax = df.get("MAX_ORDER_TOLERANCE", pd.Series(np.nan, index=df.index)).fillna(0.0)

    df["TOL_LOWER"] = df["ORDERED_QUANTITY"] * (1.0 + tmin / 100.0)
    df["TOL_UPPER"] = df["ORDERED_QUANTITY"] * (1.0 + tmax / 100.0)

    df["IS_TOL_VIOLATION"] = (
        (df["DELIVERED_QUANTITY"] < df["TOL_LOWER"]) |
        (df["DELIVERED_QUANTITY"] > df["TOL_UPPER"])
    ).fillna(False)

    df["OUTSIDE_TOL_QTY"] = 0.0
    low = df["DELIVERED_QUANTITY"] < df["TOL_LOWER"]
    high = df["DELIVERED_QUANTITY"] > df["TOL_UPPER"]
    df.loc[low, "OUTSIDE_TOL_QTY"] = (df.loc[low, "TOL_LOWER"] - df.loc[low, "DELIVERED_QUANTITY"])
    df.loc[high, "OUTSIDE_TOL_QTY"] = (df.loc[high, "DELIVERED_QUANTITY"] - df.loc[high, "TOL_UPPER"])

    if "DELIVERED_DATE" in df.columns and "PROMISED_DATE" in df.columns:
        df["DELTA_DAYS"] = (df["DELIVERED_DATE"] - df["PROMISED_DATE"]).dt.days
        df["IS_LATE"] = (df["DELTA_DAYS"] > 0).fillna(False)
    else:
        df["DELTA_DAYS"] = np.nan
        df["IS_LATE"] = False

    df["IS_OTIF_FAIL"] = (df["IS_LATE"] | df["IS_TOL_VIOLATION"]).fillna(False)
    return df

# =============================================================================
# Group tables
# =============================================================================
def group_table(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    g = df.groupby(dim, dropna=False, observed=False)

    out = pd.DataFrame({
        "dimension": dim,
        "member": g.size().index.astype(str),
        "cases": g.size().values,
        "late_rate_cases": g["IS_LATE"].mean().values,
        "tol_violation_rate_cases": g["IS_TOL_VIOLATION"].mean().values,
        "otif_fail_rate_cases": g["IS_OTIF_FAIL"].mean().values,
        "otif_fail_cases": g["IS_OTIF_FAIL"].sum().values,
    })

    if "ORDER_VALUE" in df.columns:
        total_val = g["ORDER_VALUE"].sum()
        fail_val = df.loc[df["IS_OTIF_FAIL"]].groupby(dim, dropna=False, observed=False)["ORDER_VALUE"].sum()

        out = out.merge(total_val.rename("sum_order_value"), left_on="member", right_index=True, how="left")
        out = out.merge(fail_val.rename("sum_order_value_otif_fail"), left_on="member", right_index=True, how="left")

        out["sum_order_value"] = out["sum_order_value"].fillna(0.0)
        out["sum_order_value_otif_fail"] = out["sum_order_value_otif_fail"].fillna(0.0)

        out["otif_fail_rate_value"] = np.where(
            out["sum_order_value"] != 0,
            out["sum_order_value_otif_fail"] / out["sum_order_value"],
            np.nan
        )

    return out

# =============================================================================
# Plots: Horizontal bar
# =============================================================================
def barh_rate(
    tbl: pd.DataFrame,
    metric: str,
    dim_label: str,
    filename: str,
    top_n: int = TOP_N,
    min_cases: int = MIN_CASES,
) -> None:
    if tbl.empty or metric not in tbl.columns:
        return

    t = tbl.copy()
    if min_cases is not None:
        t = t[t["cases"] >= min_cases]
    if t.empty:
        return

    t = t.sort_values(metric, ascending=False).head(top_n).copy()

    # Labels
    label = t["member"].astype(str) + " (N=" + t["cases"].astype(int).astype(str) + ")"
    if "sum_order_value" in t.columns:
        label = label + ", V=" + t["sum_order_value"].apply(fmt_int)

    fig, ax = plt.subplots(figsize=(12.5, max(4.2, 0.38 * len(t) + 1.1)))

    vals = t[metric].astype(float).values
    ax.barh(label[::-1], vals[::-1], color=PAL["mint"], edgecolor=PAL["teal"], linewidth=0.6)

    # Scale conventions: start at 0
    set_axis_from_zero(ax, "x", vals, pad=0.10)

    # Axis formatting
    ax.xaxis.set_major_formatter(PCT_FMT)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.set_xlabel("Share of cases")
    ax.set_ylabel("")

    pretty_metric = {
        "tol_violation_rate_cases": "Quantity tolerance violation rate",
        "late_rate_cases": "Late delivery rate",
        "otif_fail_rate_cases": "OTIF fail rate",
        "otif_fail_rate_value": "OTIF fail rate (value-weighted)",
    }.get(metric, metric)

    ax.set_title(f"{dim_label}: {pretty_metric} (Top {top_n}, N≥{min_cases})", color=PAL["teal"])

    style_axes(ax)
    savefig(filename)

# =============================================================================
# Plots: Meta scatter (0-based axes, percent, median lines explained)
# =============================================================================
def scatter_meta(
    tbl: pd.DataFrame,
    dim_label: str,
    filename: str,
    top_n_labels: int = 8,
    min_cases: int = MIN_CASES,
    size_col: str = "sum_order_value",
    x_col: str = "tol_violation_rate_cases",
    y_col: str = "late_rate_cases",
    show_reference_lines: bool = True,
) -> None:
    """
    Meta-Scatter:
      X = Quantity tolerance violation rate (share of cases)
      Y = Late delivery rate (share of cases)
      Bubble size = Sum order value (optional)
    """
    if tbl.empty or x_col not in tbl.columns or y_col not in tbl.columns:
        return

    t = tbl.copy()
    if min_cases is not None and "cases" in t.columns:
        t = t[t["cases"] >= min_cases]
    if t.empty:
        return

    x = t[x_col].astype(float).values
    y = t[y_col].astype(float).values

    # Bubble sizes (robust scaling)
    if size_col in t.columns:
        sizes_raw = t[size_col].fillna(0.0).astype(float).values
        s_min, s_max = np.nanmin(sizes_raw), np.nanmax(sizes_raw)
        if np.isfinite(s_min) and np.isfinite(s_max) and s_max > s_min:
            sizes = 160 + (sizes_raw - s_min) / (s_max - s_min) * (2600 - 160)
        else:
            sizes = np.full(len(t), 600.0)
    else:
        sizes = np.full(len(t), 600.0)

    fig, ax = plt.subplots(figsize=(12.8, 7.4))

    ax.scatter(
        x, y,
        s=sizes,
        alpha=0.55,
        facecolor=PAL["mint"],
        edgecolor=PAL["teal"],
        linewidths=0.9,
    )

    # Axes: start at 0 (management convention)
    set_axis_from_zero(ax, "x", x, pad=0.10)
    set_axis_from_zero(ax, "y", y, pad=0.10)

    ax.xaxis.set_major_formatter(PCT_FMT)
    ax.yaxis.set_major_formatter(PCT_FMT)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))

    ax.set_xlabel("Quantity tolerance violation rate (share of cases)")
    ax.set_ylabel("Late delivery rate (share of cases)")
    ax.set_title(
        f"{dim_label}: Late Rate vs. Quantity Tolerance Violations (Bubble = Order Value, N≥{min_cases})",
        color=PAL["teal"],
    )

    # Reference lines: medians across the plotted population (NOT targets)
    if show_reference_lines:
        x_med = float(np.nanmedian(x))
        y_med = float(np.nanmedian(y))
        ax.axvline(x_med, color=PAL["teal"], linewidth=1.2)
        ax.axhline(y_med, color=PAL["teal"], linewidth=1.2)
        # Small, explicit explanation (prevents "are these targets?" confusion)
        ax.text(
            0.01, 0.02,
            "Reference lines = median of plotted groups (not targets)",
            transform=ax.transAxes,
            ha="left", va="bottom",
            fontsize=9,
            color=PAL["mid_grey"],
        )

    # Labels: top N by order value (or cases fallback)
    if size_col in t.columns and np.isfinite(t[size_col].astype(float)).any():
        label_rank = t[size_col].astype(float)
    else:
        label_rank = t["cases"].astype(float) if "cases" in t.columns else pd.Series(np.arange(len(t)))

    idx = label_rank.sort_values(ascending=False).head(top_n_labels).index
    for i in idx:
        row = t.loc[i]
        name = str(row.get("member", ""))
        ax.annotate(
            name,
            (float(row[x_col]), float(row[y_col])),
            textcoords="offset points",
            xytext=(6, 6),
            ha="left",
            fontsize=10,
            color=PAL["text"],
        )

    style_axes(ax)
    savefig(filename)

# =============================================================================
# Conceptual 2x2 (kept, but made more consistent)
# =============================================================================
def plot_problem_classes_2x2(
    filename: str = "concept_2x2_problem_classes.png",
    title: str = "Two distinct problem classes require different management responses",
) -> None:
    fig = plt.figure(figsize=(12.8, 7.2))
    ax = plt.gca()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.02, 0.96, title, ha="left", va="top",
            fontsize=16, fontweight="bold", color=PAL["teal"])

    left, bottom, width, height = 0.08, 0.12, 0.84, 0.74

    ax.add_patch(Rectangle((left, bottom), width, height,
                           fill=False, linewidth=1.5, edgecolor=PAL["grid"]))

    ax.plot([left + width/2, left + width/2], [bottom, bottom + height],
            color=PAL["grid"], linewidth=1.5)
    ax.plot([left, left + width], [bottom + height/2, bottom + height/2],
            color=PAL["grid"], linewidth=1.5)

    ax.add_patch(FancyArrowPatch((left, bottom - 0.02), (left + width, bottom - 0.02),
                                 arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.2, color=PAL["mid_grey"]))
    ax.text(left, bottom - 0.06, "Low quantity deviation",
            ha="left", va="top", fontsize=10, color=PAL["mid_grey"])
    ax.text(left + width, bottom - 0.06, "High quantity deviation",
            ha="right", va="top", fontsize=10, color=PAL["mid_grey"])

    ax.add_patch(FancyArrowPatch((left - 0.02, bottom), (left - 0.02, bottom + height),
                                 arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.2, color=PAL["mid_grey"]))
    ax.text(left - 0.06, bottom, "Low lateness deviation",
            ha="right", va="bottom", rotation=90, fontsize=10, color=PAL["mid_grey"])
    ax.text(left - 0.06, bottom + height, "High lateness deviation",
            ha="right", va="top", rotation=90, fontsize=10, color=PAL["mid_grey"])

    # Top-left highlight (timeliness)
    tl_x, tl_y = left + 0.02, bottom + height/2 + 0.02
    tl_w, tl_h = width/2 - 0.04, height/2 - 0.04
    ax.add_patch(Rectangle((tl_x, tl_y), tl_w, tl_h,
                           facecolor=PAL["mint"], alpha=0.16,
                           edgecolor=PAL["mint"], linewidth=2.0))
    ax.text(tl_x + 0.02, tl_y + tl_h - 0.04,
            "Timeliness deviations\n(without quantity violations)",
            ha="left", va="top", fontsize=12, fontweight="bold", color=PAL["teal"])
    ax.text(tl_x + 0.02, tl_y + tl_h - 0.18,
            "• Frequent\n• Widespread across markets & plants\n• High value exposure\n• Driven by lead times, transport, execution stability",
            ha="left", va="top", fontsize=10, color=PAL["text"], linespacing=1.35)

    # Top-right highlight (quantity)
    tr_x, tr_y = left + width/2 + 0.02, bottom + height/2 + 0.02
    tr_w, tr_h = width/2 - 0.04, height/2 - 0.04
    ax.add_patch(Rectangle((tr_x, tr_y), tr_w, tr_h,
                           facecolor=PAL["gold"], alpha=0.14,
                           edgecolor=PAL["gold"], linewidth=2.0))
    ax.text(tr_x + 0.02, tr_y + tr_h - 0.04,
            "Quantity / tolerance deviations",
            ha="left", va="top", fontsize=12, fontweight="bold", color=PAL["teal"])
    ax.text(tr_x + 0.02, tr_y + tr_h - 0.14,
            "• Relatively rare\n• High severity\n• Concentrated (products, plants, carriers)",
            ha="left", va="top", fontsize=10, color=PAL["text"], linespacing=1.35)

    ax.text(left + 0.04, bottom + 0.04,
            "Low deviation zone\n(stable execution)",
            ha="left", va="bottom", fontsize=10, color=PAL["mid_grey"])

    ax.text(left + width/2 + 0.04, bottom + 0.04,
            "Mixed deviation zone\n(case-by-case root cause)",
            ha="left", va="bottom", fontsize=10, color=PAL["mid_grey"])

    savefig(filename)

# =============================================================================
# Data quality flags (unchanged, but kept)
# =============================================================================
def export_flags(df: pd.DataFrame) -> None:
    def safe_sort(d: pd.DataFrame, cols, ascending):
        cols2 = [c for c in cols if c in d.columns]
        if not cols2:
            return d
        asc2 = ascending[:len(cols2)] if isinstance(ascending, list) else ascending
        return d.sort_values(cols2, ascending=asc2)

    if "UNIT_PRICE" in df.columns:
        m = df["UNIT_PRICE"].eq(0)
        if m.any():
            out = df.loc[m].copy()
            out.insert(0, "FLAG_REASON", "UNIT_PRICE==0")
            out = safe_sort(out, ["ORDER_VALUE", "CASE_KEY"], [False, True])
            out.to_csv(FLAGS_DIR / "flag_unit_price_zero.csv", index=False)

    if "ORDER_VALUE" in df.columns:
        m = df["ORDER_VALUE"].eq(0)
        if m.any():
            out = df.loc[m].copy()
            out.insert(0, "FLAG_REASON", "ORDER_VALUE==0")
            out = safe_sort(out, ["UNIT_PRICE", "CASE_KEY"], [False, True])
            out.to_csv(FLAGS_DIR / "flag_order_value_zero.csv", index=False)

    if all(c in df.columns for c in ["ORDER_VALUE", "UNIT_PRICE", "DELIVERED_QUANTITY"]):
        approx = df["UNIT_PRICE"] * df["DELIVERED_QUANTITY"]
        rel_err = (df["ORDER_VALUE"] - approx).abs() / approx.replace(0, np.nan)
        m = rel_err.gt(0.10) & rel_err.notna()
        if m.any():
            out = df.loc[m].copy()
            out["VALUE_REL_ERR"] = rel_err.loc[m]
            out.insert(0, "FLAG_REASON", "VALUE_REL_ERR>0.10")
            out = safe_sort(out, ["VALUE_REL_ERR", "ORDER_VALUE", "CASE_KEY"], [False, False, True])
            out.to_csv(FLAGS_DIR / "flag_value_mismatch_relerr_gt_10pct.csv", index=False)

# =============================================================================
# Main
# =============================================================================
def main() -> None:
    df = try_read_csv(CSV_PATH)

    # Clean columns/strings
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].str.strip().str.strip('"')

    df = engineer_kpis(df)

    dim_candidates = [
        ("DELIVERY_COMPANY", "supplier", "Delivery Company"),
        ("FACTORY", "factory", "Factory"),
        ("PRODUCT_TYPE", "product_type", "Product Type"),
        ("FACTORY_TYPE", "factory_type", "Factory Type"),
        ("WAREHOUSE_TYPE", "warehouse_type", "Warehouse Type"),
        ("CUST_MARKET", "cust_market", "Customer Market"),
        ("CUST_COUNTRY", "cust_country", "Customer Country"),
    ]
    dims = [(d, slug, label) for d, slug, label in dim_candidates if d in df.columns]

    all_rows = []
    for dim, slug, dim_label in dims:
        tbl = group_table(df, dim)
        tbl.to_csv(TABLES_DIR / f"rates_{slug}.csv", index=False)
        all_rows.append(tbl)

        # Bars
        barh_rate(
            tbl,
            metric="tol_violation_rate_cases",
            dim_label=dim_label,
            filename=f"top{TOP_N}_{slug}_tol_violation_rate.png",
        )
        barh_rate(
            tbl,
            metric="late_rate_cases",
            dim_label=dim_label,
            filename=f"top{TOP_N}_{slug}_late_rate.png",
        )

        # Meta scatter
        scatter_meta(
            tbl,
            dim_label=dim_label,
            filename=f"meta_scatter_{slug}_late_vs_tol_bubble_value.png",
            top_n_labels=8,
            min_cases=MIN_CASES,
            show_reference_lines=True,
        )

    # Combined ranking
    if all_rows:
        otif_all = pd.concat(all_rows, ignore_index=True)
        otif_all = otif_all.sort_values(
            ["otif_fail_rate_cases", "cases"],
            ascending=[False, False],
            na_position="last",
        )
        otif_all.to_csv(OUT_DIR / "otif_ranking_all_dimensions.csv", index=False)

    export_flags(df)

    # Conceptual 2x2
    plot_problem_classes_2x2("concept_2x2_problem_classes.png")

    print("Done:")
    print("Assets root:", ASSETS_DIR.resolve())
    print("Run folder:", OUT_DIR.resolve())

if __name__ == "__main__":
    main()
