/*****
 app_favoritos functions
*/

const regex_spaces = /\s{2}/g;
const regex_nl = /\n/g

let MisFavs = {
    current_in_favs() {
        let is_in = false;
        $("#favs-menu a.fav-lnk").each((idx, lnk) => {
            if(lnk.href === location.href) {
                is_in = true;
                lnk = $(lnk);
                lnk.addClass('current-lnk');
            }
        });
        if(is_in) {
            $("button.fav-in").removeClass('d-none');
            $("button.fav-out").addClass('d-none');
        } else {
            $("button.fav-out").removeClass('d-none');
            $("button.fav-in").addClass('d-none');
        }
    },
    add2() {
        let etiqueta = $("#main-navbar-title").text().trim().replaceAll(
            regex_nl, " ").replaceAll(regex_spaces, " ");
        while(etiqueta.search(regex_spaces) > -1) {
            etiqueta = etiqueta.replaceAll(regex_spaces, " ")
        }
        let url = location.href;
        let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        $.post(set_mis_favs_url, {etiqueta, url, csrfmiddlewaretoken}, (data) => {
            $("#favs-menu").html(data);
            this.current_in_favs();
        });
    },
    delFav() {
        let pk = $("#favs-menu a.fav-lnk.current-lnk").data('lnk');
        let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        $.post(del_mis_favs_url, {pk, csrfmiddlewaretoken}, (data) => {
            $("#favs-menu").html(data);
            this.current_in_favs();
        });
    }
}

$(document).ready(() => {
    MisFavs.current_in_favs();
    $("#cntr-extra-actions").prepend($(".hidden-opc a"));
})
