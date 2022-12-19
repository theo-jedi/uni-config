import requests
from bs4 import BeautifulSoup


# express

class DependenciesVisualizer:

    def fetch(self, package_name: str, tab_level: int = 1):
        request = requests.get(f"https://www.npmjs.com/package/{package_name}/?activeTab=dependencies").content.decode()
        soup = BeautifulSoup(request, features="lxml")

        deps = soup.find("ul", {"aria-label": "Dependencies"})

        if deps is None:
            return

        for dep in deps.find_all("a"):
            dep = dep.text
            print("\t" * tab_level, package_name, " -> ", dep, sep="")
            self.fetch(dep, tab_level + 1)

    def check(self, package_name: str):
        print("Digraph {")
        self.fetch(package_name)
        print("}")


if __name__ == '__main__':
    visualizer = DependenciesVisualizer()
    while True:
        visualizer.check(input("Package name: "))
