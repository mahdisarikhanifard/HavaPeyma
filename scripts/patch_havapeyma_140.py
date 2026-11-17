import os
from pathlib import Path
root = Path(os.environ["PROJECT_DIR"])
main = root / "app/src/main/java/com/example/havapeyma/MainActivity.kt"
gradle = root / "app/build.gradle.kts"
src = main.read_text(encoding="utf-8")
def rep(old, new, label):
    global src
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {n}")
    src = src.replace(old, new, 1)

rep("    private lateinit var selectedDayAnalysis: TextView\n",
    "    private lateinit var selectedDayAnalysis: TextView\n"
    "    private lateinit var selectedDayHourly: TextView\n"
    "    private var hourlyReports: Map<String, List<HourlyForecast>> = emptyMap()\n",
    "hourly state")

rep("        dayCard.addView(selectedDayAnalysis)\n",
    "        dayCard.addView(selectedDayAnalysis)\n"
    "        dayCard.addView(actionButton(\"مشاهده هواشناسی گوگل\", 0xFF4285F4.toInt()) { openGoogleWeather() },\n"
    "            LinearLayout.LayoutParams(-2, dp(42)).apply { topMargin = dp(8) })\n"
    "        val hourlyHeading = TextView(this).apply {\n"
    "            text = \"گزارش ساعتی روز انتخاب‌شده\"; textSize = 15f\n"
    "            setTextColor(0xFF176F86.toInt())\n"
    "            setTypeface(typeface, android.graphics.Typeface.BOLD)\n"
    "            setPadding(0, dp(12), 0, dp(4))\n"
    "        }\n"
    "        dayCard.addView(hourlyHeading)\n"
    "        selectedDayHourly = sectionText(13f, 0xFF294F5C.toInt())\n"
    "        dayCard.addView(selectedDayHourly)\n",
    "day card UI")

rep("&hourly=temperature_2m,precipitation_probability,uv_index,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=",
    "&hourly=temperature_2m,precipitation,precipitation_probability,uv_index,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=",
    "hourly precipitation request")

rep('                val hRain = hourlyData.optJSONArray("precipitation_probability")\n',
    '                val hRain = hourlyData.optJSONArray("precipitation_probability")\n'
    '                val hPrecip = hourlyData.optJSONArray("precipitation")\n',
    "hourly precipitation parse")

rep('                val hWindGust = hourlyData.optJSONArray("wind_gusts_10m")\n',
    '                val hWindGust = hourlyData.optJSONArray("wind_gusts_10m")\n'
    '                val hourlyByDate = linkedMapOf<String, MutableList<HourlyForecast>>()\n'
    '                if (hTimes != null && hTemps != null) {\n'
    '                    for (i in 0 until minOf(hTimes.length(), hTemps.length())) {\n'
    '                        val timestamp = hTimes.optString(i)\n'
    '                        val date = timestamp.take(10)\n'
    '                        if (date.length != 10) continue\n'
    '                        hourlyByDate.getOrPut(date) { mutableListOf() }.add(\n'
    '                            HourlyForecast(\n'
    '                                time = timestamp.substringAfter("T", "--:--").take(5),\n'
    '                                temperature = hTemps.optDouble(i, Double.NaN),\n'
    '                                precipitation = hPrecip?.optDouble(i, Double.NaN) ?: Double.NaN,\n'
    '                                precipitationProbability = hRain?.optDouble(i, Double.NaN) ?: Double.NaN,\n'
    '                                windSpeed = hWind?.optDouble(i, Double.NaN) ?: Double.NaN,\n'
    '                                windDirection = hWindDir?.optDouble(i, Double.NaN) ?: Double.NaN,\n'
    '                                windGust = hWindGust?.optDouble(i, Double.NaN) ?: Double.NaN\n'
    '                            )\n'
    '                        )\n'
    '                    }\n'
    '                }\n',
    "hourly forecast grouping")

rep("                    locationToday = currentLocationDate\n",
    "                    locationToday = currentLocationDate\n"
    "                    hourlyReports = hourlyByDate\n",
    "hourly report state assignment")

rep("    private fun updateSelectedDayAnalysis() {\n",
    "    private fun openGoogleWeather() {\n"
    '        val query = if (selectedForecastDate.isBlank()) "weather in $city" else "weather in $city on $selectedForecastDate"\n'
    '        val url = "https://www.google.com/search?q=" + URLEncoder.encode(query, "UTF-8")\n'
    "        try {\n"
    "            startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse(url)))\n"
    "        } catch (e: Exception) {\n"
    '            Toast.makeText(this, "امکان باز کردن جست‌وجوی گوگل وجود ندارد", Toast.LENGTH_SHORT).show()\n'
    "        }\n"
    "    }\n\n"
    "    private fun updateSelectedDayAnalysis() {\n",
    "Google Weather public search action")

rep('            if (actual == null) append("\\nمبنای سال کشاورزی: ۱ مهر تا پایان شهریور؛ مجموع واقعی فقط در صورت دریافت داده تاریخی معتبر نمایش داده می‌شود.")\n'
    "        }\n",
    '            if (actual == null) append("\\nمبنای سال کشاورزی: ۱ مهر تا پایان شهریور؛ مجموع واقعی فقط در صورت دریافت داده تاریخی معتبر نمایش داده می‌شود.")\n'
    "        }\n"
    "        val hours = hourlyReports[selectedForecastDate].orEmpty()\n"
    "        selectedDayHourly.text = if (hours.isEmpty()) {\n"
    '            "گزارش ساعتی این روز در دسترس نیست."\n'
    "        } else buildString {\n"
    '            append("ساعت  |  دما  |  بارش  |  احتمال بارش  |  باد  |  تندباد\\n")\n'
    "            hours.forEach { hour ->\n"
    '                append("${hour.time}  |  ${format(hour.temperature)}°C  |  ${formatMm(hour.precipitation)} mm  |  ")\n'
    '                append("${format(hour.precipitationProbability)}٪  |  ${format(hour.windSpeed)} km/h ${windDirectionText(hour.windDirection)}  |  ${format(hour.windGust)} km/h\\n")\n'
    "            }\n"
    "        }\n",
    "hourly report renderer")

rep("    private data class DayForecast(\n",
    "    private data class HourlyForecast(\n"
    "        val time: String, val temperature: Double, val precipitation: Double,\n"
    "        val precipitationProbability: Double, val windSpeed: Double,\n"
    "        val windDirection: Double, val windGust: Double\n"
    "    )\n\n"
    "    private data class DayForecast(\n",
    "hourly forecast model")

main.write_text(src, encoding="utf-8")
g = gradle.read_text(encoding="utf-8")
if 'versionName = "1.3.7"' not in g or "versionCode = 13" not in g:
    raise SystemExit("Unexpected base version; refusing unsafe version bump")
g = g.replace('versionName = "1.3.7"', 'versionName = "1.4.0"', 1)
g = g.replace("versionCode = 13", "versionCode = 16", 1)
gradle.write_text(g, encoding="utf-8")
print("Patched HavaPeyma 1.4.0: selected-day hourly rendering fixed; widget refresh routed through a dedicated receiver.")


# Route manual widget refreshes through one explicit, manifest-registered receiver.
widget = root / "app/src/main/java/com/example/havapeyma/WeatherWidgetProvider.kt"
ws = widget.read_text(encoding="utf-8")
old = '''        val refreshIntent = Intent(context, javaClass).setAction(ACTION_UPDATE_WIDGET)
            .putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, id)
        views.setOnClickPendingIntent(R.id.widget_refresh, PendingIntent.getBroadcast(context, id * 10 + 3, refreshIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE))'''
new = '''        val refreshIntent = Intent(context, WidgetRefreshReceiver::class.java)
            .setAction(WidgetRefreshReceiver.ACTION_MANUAL_REFRESH)
        views.setOnClickPendingIntent(R.id.widget_refresh, PendingIntent.getBroadcast(context, id * 10 + 3, refreshIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE))'''
if ws.count(old) != 1:
    raise SystemExit(f"widget refresh PendingIntent anchor count: {ws.count(old)}")
ws = ws.replace(old, new, 1)
receiver_src = main.read_text(encoding="utf-8")
old = '''        val update = Intent(WeatherWidgetProvider.ACTION_UPDATE_WIDGET).setPackage(context.packageName)
        context.sendBroadcast(update)
    }
    companion object { const val ACTION_TICK = "com.example.havapeyma.WIDGET_REFRESH_TICK" }'''
new = '''        val providers = listOf(
            SmallWeatherWidgetProvider::class.java,
            MediumWeatherWidgetProvider::class.java,
            LargeWeatherWidgetProvider::class.java
        )
        providers.forEach { provider ->
            context.sendBroadcast(
                Intent(WeatherWidgetProvider.ACTION_UPDATE_WIDGET).setClass(context, provider)
            )
        }
    }
    companion object {
        const val ACTION_TICK = "com.example.havapeyma.WIDGET_REFRESH_TICK"
        const val ACTION_MANUAL_REFRESH = "com.example.havapeyma.WIDGET_MANUAL_REFRESH"
    }'''
if receiver_src.count(old) != 1:
    raise SystemExit(f"widget receiver anchor count: {receiver_src.count(old)}")
receiver_src = receiver_src.replace(old, new, 1)
main.write_text(receiver_src, encoding="utf-8")

