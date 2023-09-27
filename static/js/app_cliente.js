/*****
 app_cliente functions
*/

let open_nota_panel = (can_read, can_add) => {
    let template = Handlebars.compile($("#modal-content-notas-template").html());
    let html = template({can_read, can_add});
    App.openPanel(html, "Notas del Cliente");
}

let open_alerta_panel = (can_add) => {
    let template = Handlebars.compile($("#modal-content-alertas-template").html());
    let html = template({can_add});
    App.openPanel(html, "Alertas del Cliente");
}
