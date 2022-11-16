import scrapy
from scrapy.selector import Selector

class Deps(scrapy.Spider):
    name = "depsf"
    f = open('links\lista_deputadas.txt', 'r')
    start_urls = f.readlines()
        
    def parse(self, response):
        retorno = dict()
        proximas = []
        nome_nascimento = response.css("ul.informacoes-deputado").getall()
        nome_nascimento = Selector(text=nome_nascimento[0]).xpath('//li/text()').getall()

        retorno["nome"] = nome = nome_nascimento[0]
        retorno["genero"] = "F"
        retorno["presenca_plenario"] = response.css(".list-table__item:nth-child(1) .list-table__definition-description:nth-child(2)::text").get().replace("\n", "").replace(" ", "").replace("dias", "")
        retorno["ausencia_plenario"] = response.css(".list-table__item:nth-child(1) .list-table__definition-description:nth-child(6)::text").get().replace("\n", "").replace(" ", "").replace("dias", "")
        retorno["ausencia_justificada_plenario"] = response.css(".list-table__item:nth-child(1) .list-table__definition-description:nth-child(4)::text").get().replace("\n", "").replace(" ", "").replace("dias", "")
        retorno["presenca_comissao"] = response.css(".list-table__item+ .list-table__item .list-table__definition-description:nth-child(2)::text").get().replace("\n", "").replace(" ", "").replace("reuniões", "")
        retorno["ausencia_comissao"] = response.css(".list-table__item+ .list-table__item .list-table__definition-description:nth-child(6)::text").get().replace("\n", "").replace(" ", "").replace("reuniões", "")
        retorno["ausencia_justificada_comissao"] = response.css(".list-table__item+ .list-table__item .list-table__definition-description:nth-child(4)::text").get().replace("\n", "").replace(" ", "").replace("reuniões", "")
        retorno["data_nascimento"] = nome_nascimento[4]
        retorno["salario_bruto"] = response.css("li:nth-child(2) .beneficio__info::text").get().replace("\n", "").replace(" ", "").replace('R$', '')
        retorno["quant_viagem"] = response.css(".beneficio__viagens .beneficio__info::text").get()
        retorno["gasto_total_gab"] = response.css(".gasto+ .gasto .gasto__col:nth-child(1) tr:nth-child(1) td:nth-child(2)::text").get()

        proximas.append(response.css(".gasto+ .gasto .veja-mais__item::attr(href)").get())
        proximas.append(response.css(".gasto:nth-child(1) .veja-mais__item::attr(href)").get())

        request_gab = scrapy.Request(proximas[0],
                            callback=self.parse_gasto_gab, cb_kwargs=dict(proxima=proximas[1], retorno=retorno))

        yield request_gab

    def parse_gasto_gab(self, response, proxima, retorno):
        gastos = []
        for i in range(1, 13):
            idx = str(i)
            if i == 1:
                gasto_mes = response.css('tr:nth-child(1) .alinhar-direita+ td::text').get()
            else:
                gasto_mes = response.css(f'tr:nth-child({idx}) .alinhar-direita+ .alinhar-direita::text').get()
        
            if gasto_mes:
                gasto_mes = gasto_mes.replace("\n", "").replace(" ", "").replace('\tR$', '').replace('\t', '')
            else:
                gasto_mes = '0'       
            gastos.append(gasto_mes)

        retorno['gasto_jan_gab'] = gastos[0]
        retorno['gasto_fev_gab'] = gastos[1]
        retorno['gasto_mar_gab'] = gastos[2]
        retorno['gasto_abr_gab'] = gastos[3]
        retorno['gasto_maio_gab'] = gastos[4]
        retorno['gasto_junho_gab'] = gastos[5]
        retorno['gasto_jul_gab'] = gastos[6]
        retorno['gasto_agosto_gab'] = gastos[7]
        retorno['gasto_set_gab'] = gastos[8]
        retorno['gasto_out_gab'] = gastos[9]
        retorno['gasto_nov_gab'] = gastos[10]
        retorno['gasto_dez_gab'] = gastos[11]

        request_par = scrapy.Request(proxima,
                            callback=self.parse_gasto_par, cb_kwargs=dict(retorno=retorno))
        
        yield request_par

    def parse_gasto_par(self, response, retorno):
        gasto_total = response.css('#totalFinalAgregado::text').get().replace("\n", "").replace(" ", "").replace('\tR$', '')
        
        gastos = []
        for i in range(0, 12):
            if i < 10:
                idx = '0' + str(i)
            else:
                idx = str(i)

            gasto_mes = response.css(f"#nivel2Total{idx}::text").get()
        
            if gasto_mes:
                gasto_mes = gasto_mes.replace("\n", "").replace(" ", "").replace('\tR$', '').replace('\t', '')
            else:
                gasto_mes = '0' 
            gastos.append(gasto_mes)
        
        retorno['gasto_total_par'] = gasto_total
        retorno['gasto_jan_par'] = gastos[0]
        retorno['gasto_fev_par'] = gastos[1]
        retorno['gasto_mar_par'] = gastos[2]
        retorno['gasto_abr_par'] = gastos[3]
        retorno['gasto_maio_par'] = gastos[4]
        retorno['gasto_junho_par'] = gastos[5]
        retorno['gasto_jul_par'] = gastos[6]
        retorno['gasto_agosto_par'] = gastos[7]
        retorno['gasto_set_par'] = gastos[8]
        retorno['gasto_out_par'] = gastos[9]
        retorno['gasto_nov_par'] = gastos[10]
        retorno['gasto_dez_par'] = gastos[11]

        yield retorno
