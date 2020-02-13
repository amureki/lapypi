from chalice import Chalice, Response
from jinja2 import Environment, PackageLoader, select_autoescape

app = Chalice(app_name='chalk')

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


@app.route('/')
def index():
    template = env.get_template('index.html')
    return Response(body=template.render(go='Ha-HA'),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})


@app.route('/simple/{package_name}')
def index(package_name):
    template = env.get_template('package.html')
    return Response(body=template.render(package_name=package_name),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})


@app.route('/simple', methods=['GET', 'POST'])
def simple():
    template = env.get_template('simple.html')
    package_list = ['django', 'flask']
    return Response(body=template.render(package_list=package_list),
                    status_code=200,
                    headers={'Content-Type': 'text/html'})
