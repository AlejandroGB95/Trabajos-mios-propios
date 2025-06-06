from django.core.management.base import BaseCommand
from monitor.models import UrlMonitor  

class Command(BaseCommand):
    help = "Carga inicial de URLs"

    def handle(self, *args, **kwargs):
        urls = [
            'https://www.xunta.gal/dog/Publicados/2025/20250409/Indice69_gl.pdf',
            'https://sede.asturias.es/bopa/2025/04/09/20250409.pdf',
            'https://boc.cantabria.es/boces/verPdfAction.do?idBlob=39943&tipoPdf=0',
            'https://www.euskadi.eus/web01-bopv/es/bopv2/datos/2025/04/s25_0069.pdf',
            'https://ias1.larioja.org/boletin/Bor_Boletin_visor_Servlet?referencia=34191265-2-X',
            'https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1387843610202',
            'https://bocyl.jcyl.es/boletines/2025/04/09/pdf/BOCYL-S-09042025.pdf',
            'https://www.bocm.es/boletin/CM_Boletin_BOCM/2025/04/09/08400.PDF',
            'https://docm.jccm.es/docm/descargarArchivo.do?ruta=2025/04/04/pdf/docm_66.pdf&tipo=rutaDocm',
            'https://doe.juntaex.es/pdfs/doe/2025/690o/690o.pdf',
            'https://dogv.gva.es/datos/2025/04/09/pdf/dogv_2025_10084_es.pdf',
            'https://www.borm.es/services/boletin/ano/2025/numero/82/pdf',
            'https://www.juntadeandalucia.es/eboja/2025/68/BOJA25-068-00013_10000038.pdf',
            'https://www.ceuta.es/ceuta/component/jdownloads/finish/1954-abril/22784-bocce-extra14-08-04-2025?Itemid=534',
        ]

        for url in urls:
            UrlMonitor.objects.get_or_create(url=url)

        self.stdout.write(self.style.SUCCESS("URLs precargadas correctamente"))
