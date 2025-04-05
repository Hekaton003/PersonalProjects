from django.shortcuts import render
from django.views.generic import ListView
from .models import Watch
from django.core.paginator import Paginator


# Create your views here.

class ProductListView(ListView):
    model = Watch
    template_name = "product/Home.html"
    context_object_name = "watches"
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        category = self.request.GET.get("selected_category")
        if category:
            queryset = queryset.filter(name__iexact=category)

        max_price = self.request.GET.get('max_price')

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add current filters to context
        context['max_price'] = self.request.GET.get('max_price', '')
        context['selected_category'] = self.request.GET.get('selected_category')
        categories = [name for name in Watch.objects.values_list('name', flat=True).distinct()]
        context['categories'] = categories
        return context


def about_page(request):
    return render(request, "product/about-us.html", context={'isAbout': True})


def location_page(request):
    stores = [
        {"name": "Schroll Kitzbühel",
         "image": "https://content.rolex.com/v7/dam/rolex-retailers/store-locator/store-pages/store-details/store-details-generic-02.jpg",
         "address": "Vorderstadt 23, 6370 Kitzbühel, Austria"},
        {"name": "Schullin GmbH",
         "image": "https://content.rolex.com/rocc/assets/RSWI_1444/portrait-v6.jpg?imwidth=800",
         "address": "Herrengasse 3, 8010 Graz, Austria"},
        {"name": "Malalan D.O.O.",
         "image": "https://content.rolex.com/rocc/assets/RSWI_2383/portrait-v6.jpg?imwidth=800",
         "address": "Mestni trg 21, 1000 Ljubljana, Slovenia"},
        {"name": "Petite Geneve Petrovic",
         "image": "https://content.rolex.com/v7/dam/rolex-retailers/store-locator/store-pages/store-details/store-details-generic-01.jpg",
         "address": "Uskocka 7, 11000 Belgrade, Serbia"},
        {"name": "PETITE GENEVE PETROVIC (MONTENEGRO DOO)",
         "image": "https://content.rolex.com/rocc/assets/RSWI_17865/portrait-v6.jpg?imwidth=800",
         "address": "Blaža Jovanovića br. 1 (Hotel Regent), 85320 Tivat, Montenegro"},
        {"name": "Besha Rolex Boutique‬",
         "image": "https://content.rolex.com/v7/dam/rolex-retailers/store-locator/store-pages/store-details/store-details-generic-01.jpg",
         "address": "Boulevard Vitosha 34, 1000 Sofia, Bulgaria"},
        {"name": "IOANNIDIS JEWELLERY",
         "image": "https://content.rolex.com/rocc/assets/RSWI_1467/portrait-v6.jpg?imwidth=800",
         "address": "41 Nikiforou Theotoki, 49100 Corfu, Greece"},
        {"name": "Passo A.S. / Sheron",
         "image": "https://content.rolex.com/v7/dam/rolex-retailers/store-locator/store-pages/store-details/store-details-generic-01.jpg",
         "address": "Panska 2, 811 01 Bratislava, Slovakia"},
        {"name": "Curnis", "image": "https://content.rolex.com/rocc/assets/RSWI_1884/portrait-v6.jpg?imwidth=800",
         "address": "Via Monte Grappa 7, 24121 Bergamo, Italy"},
        {"name": "Tomasi",
         "image": "https://content.rolex.com/v7/dam/rolex-retailers/store-locator/store-pages/store-details/store-details-generic-03.jpg",
         "address": "Via S. Pietro 1, 38100 Trento, Italy"},
        {"name": "Michaud Verbier",
         "image": "https://content.rolex.com/rocc/assets/RSWI_16475/portrait-v6.jpg?imwidth=800",
         "address": "5 Rue de Médran, 1936 Verbier, Switzerland"},
        {"name": "Frojo", "image": "https://content.rolex.com/rocc/assets/RSWI_9515/portrait-v6.jpg?imwidth=800",
         "address": "Valstore, 73150 Val d'Isère, France"},
    ]
    paginator = Paginator(stores, 6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "product/location.html", context={'page_obj': page_obj})


def contact_page(request):
    return render(request, "product/contact.html")


def tennis_page(request):
    return render(request, "product/tennis.html")


def golf_page(request):
    return render(request, "product/golf.html")


def yacht_page(request):
    return render(request, "product/yacht.html")


def moto_page(request):
    return render(request, "product/moto.html")


def cinema_page(request):
    return render(request, "product/cinema.html")


def music_page(request):
    return render(request, "product/music.html")


def architecture_page(request):
    buildings = [
        {
            "image": "https://static1.straitstimes.com.sg/s3fs-public/articles/2023/07/13/Centenary%20Hall%20Rolex%20Australia%20HQ.jpg?VersionId=k8xXnNr.5WByZH4WZ1Opg4YrIdDwTrAb",
            "title": "Melbourne, Australia",
            "description": "A global architecture studio",
            "author": "Woods Bagot"
        },
        {
            "image": "https://distribution-point.webstorage-4sigma.it/redesco2022/media/progetto/2023/IMG_20200525_120906-1920x1440.jpg",
            "title": "Milan, Italy",
            "description": "An architectural practice based in Milano, Italia.",
            "author": "Onsitestudio"
        },
        {
            "image": "https://images.rolex.org/data/media/img/arts/a-dynamic-tower-for-dallas/desktop_0002.jpg",
            "title": "Texas, USA",
            "description": "Japanese architect and emeritus professor in the Department of Architecture (Graduate School of Engineering) at the University of Tokyo",
            "author": "Kengo Kuma"
        },
        {
            "image": "https://sdg-migration-id.s3.amazonaws.com/145808-rolex4.jpg",
            "title": "Lausanne, Switzerland",
            "description": "An architectural firm based in Tokyo",
            "author": "SANAA"
        },
        {
            "image": "https://images.rolex.org/data/media/img/science/an-education-in-precision/desktop_0002.jpg",
            "title": "Pennsylvania, USA",
            "description": "An American architect, designer, and educator",
            "author": "Michael Graves"
        },
        {
            "image": "https://media.rolex.com/image/upload/q_auto:eco/f_auto/c_limit,w_1920/v1708408423/rolexcom/perpetual-arts/rolex-and-architecture/a-commitment-to-precision/roller/rolex-and-arts-architecture-a-commitment-to-precision-toyocho-japan2003-001",
            "title": "Tokyo, Japan",
            "description": "A Japanese architect known for fusing modernism with Japanese architectural traditions.",
            "author": "Fumihiko Maki"
        }
    ]
    paginator = Paginator(buildings, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "product/architecture.html", context={"objects": page_obj})
