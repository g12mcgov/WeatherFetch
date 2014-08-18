## Contains email body

import jinja2

def constructTemplate(forecast_io_hourly, wunderground_hourly, hamweather_hourly, weather_map, current_average, max_average, min_average, pop):
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "Users/grantmcgovern/Dropbox/Developer/Projects/WeatherFetch/backend/src/email/email.jinja"
    template = templateEnv.get_template(TEMPLATE_FILE)
    templateVars = {'current_average':current_average}
    email = template.render(templateVars)

    return email 