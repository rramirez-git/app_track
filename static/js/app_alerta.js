/*****
 app_alerta functions
*/

$(document).ready(() => {
    if("string" == typeof app_alertas_get_url) {
        $.get(app_alertas_get_url, (alertas) => {
            if(alertas.length > 0) {
                let div_contenedor = $(`<div style="padding: 1rem;"></div>`);
                alertas.forEach(alerta => {
                    let template = Handlebars.compile(
                        $( "#app_alerta-alerta-template" ).html() );
                    let html = template( { 
                        "nota": alerta.nota, 
                        "csrf_token": $(`#csrf_token`).html(), 
                        "url": app_alertas_disabled_url.replaceAll("_pk_", alerta.pk)});
                    div_contenedor.prepend(html);
                    });
                $(`div.bs-offset-main.bs-canvas-anim`).prepend(div_contenedor);
                };
        }, 'json').fail((jqXHR, textStatus, errorThrown)=>{ 
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        });
    }
})



