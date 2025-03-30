def format_change(change):
    return f"📈 +{change:.2f}%" if change >= 0 else f"📉 {change:.2f}%"