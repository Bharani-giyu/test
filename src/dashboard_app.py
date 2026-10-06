from __future__ import annotations

from nicegui import ui


DATA = {
    "All regions": {
        "label": "All regions",
        "cards": {
            "Revenue": {"value": "$1.48M", "delta": "+12.4%", "trend": "vs last month"},
            "Users": {"value": "84.2K", "delta": "+8.7%", "trend": "new signups"},
            "Conversion": {"value": "6.6%", "delta": "+1.1 pts", "trend": "last 30 days"},
            "CSAT": {"value": "4.8/5", "delta": "+0.3", "trend": "customer score"},
        },
        "series": [64, 70, 68, 82, 88, 94, 92],
    },
    "North": {
        "label": "North",
        "cards": {
            "Revenue": {"value": "$430K", "delta": "+16.1%", "trend": "vs last month"},
            "Users": {"value": "24.4K", "delta": "+10.3%", "trend": "new signups"},
            "Conversion": {"value": "7.1%", "delta": "+1.3 pts", "trend": "last 30 days"},
            "CSAT": {"value": "4.9/5", "delta": "+0.2", "trend": "customer score"},
        },
        "series": [52, 60, 58, 75, 86, 92, 98],
    },
    "South": {
        "label": "South",
        "cards": {
            "Revenue": {"value": "$360K", "delta": "+10.9%", "trend": "vs last month"},
            "Users": {"value": "20.7K", "delta": "+8.1%", "trend": "new signups"},
            "Conversion": {"value": "6.1%", "delta": "+0.8 pts", "trend": "last 30 days"},
            "CSAT": {"value": "4.7/5", "delta": "+0.1", "trend": "customer score"},
        },
        "series": [48, 55, 63, 72, 79, 81, 87],
    },
    "West": {
        "label": "West",
        "cards": {
            "Revenue": {"value": "$390K", "delta": "+13.2%", "trend": "vs last month"},
            "Users": {"value": "22.6K", "delta": "+9.5%", "trend": "new signups"},
            "Conversion": {"value": "6.7%", "delta": "+1.0 pts", "trend": "last 30 days"},
            "CSAT": {"value": "4.8/5", "delta": "+0.4", "trend": "customer score"},
        },
        "series": [58, 62, 67, 78, 84, 90, 94],
    },
    "East": {
        "label": "East",
        "cards": {
            "Revenue": {"value": "$300K", "delta": "+11.4%", "trend": "vs last month"},
            "Users": {"value": "16.5K", "delta": "+7.2%", "trend": "new signups"},
            "Conversion": {"value": "6.3%", "delta": "+0.9 pts", "trend": "last 30 days"},
            "CSAT": {"value": "4.6/5", "delta": "+0.2", "trend": "customer score"},
        },
        "series": [43, 49, 55, 64, 72, 77, 82],
    },
}


def build_chart_svg(series: list[int]) -> str:
    width = 540
    height = 220
    padding_x = 20
    padding_y = 22
    max_value = max(series)
    min_value = min(series)
    if max_value == min_value:
        max_value += 1

    x_step = (width - padding_x * 2) / (len(series) - 1) if len(series) > 1 else 1
    points = []
    for index, value in enumerate(series):
        x = padding_x + index * x_step
        y = height - padding_y - ((value - min_value) / (max_value - min_value + 0.0001)) * (height - padding_y * 2)
        points.append(f"{x:.1f},{y:.1f}")

    path = "M " + " L ".join(points)
    area_path = f"{path} L {width - padding_x},{height - padding_y} L {padding_x},{height - padding_y} Z"

    return f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Performance chart">
      <defs>
        <linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#4f46e5" stop-opacity="0.32"/>
          <stop offset="100%" stop-color="#4f46e5" stop-opacity="0.02"/>
        </linearGradient>
      </defs>
      <g fill="none" stroke="#dbe3f0" stroke-width="1">
        <path d="M {padding_x} {padding_y} L {padding_x} {height - padding_y}" />
        <path d="M {padding_x} {height - padding_y} L {width - padding_x} {height - padding_y}" />
      </g>
      <path d="{area_path}" fill="url(#chartFill)" />
      <path d="{path}" fill="none" stroke="#4f46e5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
      {''.join(f'<circle cx="{padding_x + i * x_step:.1f}" cy="{height - padding_y - ((v - min_value) / (max_value - min_value + 0.0001)) * (height - padding_y * 2):.1f}" r="4" fill="#4f46e5" />' for i, v in enumerate(series))}
    </svg>
    """


def build_dashboard() -> None:
    @ui.page("/")
    def dashboard_page() -> None:
        with ui.column().classes("w-full max-w-6xl mx-auto p-4 md:p-8 gap-4"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-1"):
                    ui.label("Operations dashboard").classes("text-3xl font-bold text-slate-900")
                    ui.label("Portfolio overview and KPI momentum").classes("text-sm text-slate-500")
                ui.select(
                    label="Filter by region",
                    options=["All regions", "North", "South", "West", "East"],
                    value="All regions",
                    with_input=False,
                    on_change=lambda e: render_summary(e.value),
                ).classes("w-52")

            summary_container = ui.row().classes("w-full gap-4 flex-wrap")
            chart_holder = ui.element("div").classes("w-full")

            def render_summary(region_name: str) -> None:
                summary_container.clear()
                data = DATA[region_name]
                cards = list(data["cards"].items())

                with summary_container:
                    for title, values in cards:
                        with ui.card().classes("flex-1 min-w-[180px] p-4 shadow-sm border border-slate-200 bg-white"):
                            ui.label(title).classes("text-sm uppercase tracking-wide text-slate-500")
                            ui.label(values["value"]).classes("text-3xl font-bold text-slate-900 mt-2")
                            with ui.row().classes("items-center mt-2 gap-2"):
                                ui.badge(values["delta"]).classes("bg-emerald-100 text-emerald-700 text-xs font-semibold")
                                ui.label(values["trend"]).classes("text-xs text-slate-500")

                chart_holder.clear()
                with chart_holder:
                    with ui.card().classes("w-full p-4 border border-slate-200 shadow-sm bg-white"):
                        with ui.row().classes("items-center justify-between mb-3"):
                            ui.label(f"{data['label']} momentum").classes("text-lg font-semibold text-slate-800")
                            ui.badge("+12.4% QoQ").classes("bg-violet-100 text-violet-700 text-xs font-semibold")
                        ui.html(build_chart_svg(data["series"]))

            render_summary("All regions")


if __name__ == "__main__":
    build_dashboard()
