let dataGridResultsGlobals = {
    __table: null,
    __header: null,
    __body: null,
    __columns: [],
    __hidden_cols: [],
    init(table, updatingtable = false) {
        this.__table = table;
        this.__header = this.__table.find("thead");
        this.__body = this.__table.find("tbody");
        let real_header_finder = (this.__header.find("tr:first-child th").length > 0 ) ? "tr:first-child th" : "tr:nth-child(2) th";
        this.__header.find(real_header_finder).each((index, element) => {
            element = $(element);
            this.__columns.push({
                idx: index,
                label: element.text().trim(),
                is_sorteable: "yes" === String(element.data('dgr-col-sorteable')).toLowerCase(),
                is_hiddenable: "yes" === String(element.data('dgr-col-hiddenable')).toLowerCase(),
                is_filterable: "yes" === String(element.data('dgr-col-filterable')).toLowerCase(),
                is_link_to_detail: "yes" === String(element.data('dgr-col-link-detail')).toLowerCase(),
                datatype: String(element.data('dgr-col-datatype')),
                cell: element
            });
        });
        this.__table.find("tfoot").remove();
        for(let opc of [
            {id: 'opc-print', fn: 'to_printer', label: 'Imprimir', extraClass: ''},
            {id: 'opc-to-excel', fn: 'to_excel', label: 'Excel', extraClass: ''},
            {id: 'opc-show-edit-controls', fn: 'show_edit_controls', label: 'Editar', extraClass: ''},
            {id: 'opc-hide-edit-controls', fn: 'hide_edit_controls', label: 'Cerrar Edicion', extraClass: 'd-none'},
            {id: 'opc-show-filter-controls', fn: 'show_filter_controls', label: 'Filtrar', extraClass: ''},
            {id: 'opc-hide-filter-controls', fn: 'hide_filter_controls', label: 'Cerrar Filtrado', extraClass: 'd-none'},
        ]) {
            $("#cntr-extra-actions").append(
                `<a id="${opc.id}" class="dropdown-item ${opc.extraClass}" href="#" onclick="dataGridResultsGlobals.${opc.fn}()">${opc.label}</a>`);
        }
        if(updatingtable){
            this.set_sorteable();
            this.set_filterable();
            this.set_link2detail();
            let btnToggleCols = $(`button[data-action="toggle-cols"]`);
            if(btnToggleCols.length) {
                let cntr = $("#cntr-extra-actions");
                let template = Handlebars.compile($("#tpl-toggler-cols-submenu").html());
                let html = $(template({columns: this.cols.hiddenable()}));
                html.find("input[type=checkbox]").bootstrapToggle();
                cntr.append(html);
                btnToggleCols.remove();
            }
        }
    },
    cols: {
        sorteable() { return dataGridResultsGlobals.__columns.filter(column => column.is_sorteable); },
        hiddenable() { return dataGridResultsGlobals.__columns.filter(column => column.is_hiddenable); },
        filterable() { return dataGridResultsGlobals.__columns.filter(column => column.is_filterable); },
        link2detail() { return dataGridResultsGlobals.__columns.filter(column => column.is_link_to_detail); }
    },
    set_sorteable() { this.cols.sorteable().forEach(columna => {
        columna.cell.click(() => this.sort_report(columna.idx, columna.datatype));
        columna.cell.css('cursor', 'pointer');
        columna.cell.prepend($(`<i class="fas fa-sort-down float-right d-none sort-sign-asc"></i>`));
        columna.cell.prepend($(`<i class="fas fa-sort-up float-right d-none sort-sign-desc"></i>`));
    }) },
    set_filterable() {
        let template, html, i, cells = [];
        this.__header.find("#filter-row").remove();
        for(i = 0; i < this.__columns.length; i++) {
            if(i == (this.__columns.length - 1)){
                template = Handlebars.compile($("#tpl-filter-last-cell").html());
            } else if(this.__columns[i].is_filterable) {
                template = Handlebars.compile($("#tpl-filter-cell").html());
            } else {
                template = Handlebars.compile($("#tpl-filter-empty-cell").html());
            }
            cells.push(template({column_number: this.__columns[i].idx}));
        }
        template = Handlebars.compile($("#tpl-filter-row").html());
        this.__header.append($(template({cells})));
        this.__header.find(`input[type="text"]`).keyup(dataGridResultsGlobals.apply_filter);
    },
    set_link2detail() {
        let trs = this.__body.find('tr');
        for(column of this.cols.link2detail()){
            for(tr of trs) {
                tr = $(tr);
                let cell = tr.find(`td:nth-child(${column.idx + 1})`);
                let label = cell.text().trim();
                let url = url_read.replace('__recordid__', tr.data('dgr-object-id'))
                let link = `<a class="main-col-link" href="${url}">${label}</a>`;
                cell.html(link);
            }
        }
    },
    sort_report(column_number, datatype) {
        let i, shouldSwitch, x, y, tmp, switchcount = 0;
        this.__header.find(".sort-sign-asc, .sort-sign-desc").addClass('d-none');
        let switching = true;
        let dir = "asc";
        while (switching) {
            switching = false;
            let rows =  this.__body.find("tr");
            for(i = 0; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                tmp = $(rows[i]).find(`td:nth-child(${column_number + 1})`).data('dgr-raw-sort-value');
                x = ("number" === datatype ? Number(tmp) : String(tmp));
                tmp = $(rows[i + 1]).find(`td:nth-child(${column_number + 1})`).data('dgr-raw-sort-value');
                y = ("number" === datatype ? Number(tmp) : String(tmp));
                if(("asc" === dir && x > y)||("desc" === dir && x < y)) {
                    shouldSwitch = true;
                    break;
                }
            }
            if(shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                switchcount++;
            } else if(0 == switchcount && "asc" === dir) {
                dir = "desc";
                switching = true;
            }
        }
        if("asc" === dir) {
            this.__header.find(`th:nth-child(${column_number + 1}) .sort-sign-asc`).removeClass('d-none');
        } else if("desc" === dir) {
            this.__header.find(`th:nth-child(${column_number + 1}) .sort-sign-desc`).removeClass('d-none');
        }
    },
    clear_filter() {
        this.__header.find(`input[type="text"]`).val("");
        this.__body.find("tr.d-none").removeClass("d-none");
    },
    apply_filter() {
        console.log(`Filtering`);
        let inputs = dataGridResultsGlobals.__header.find(`input[type="text"]`);
        let trs = dataGridResultsGlobals.__body.find('tr');
        trs.removeClass('d-none');
        for (let input of inputs) {
            input = $(input);
            let filter_by = String(input.val()).toLowerCase();
            let col_number = Number(input.data('column'));
            if ("" === filter_by) {
                continue;
            }
            for (let tr of trs) {
                tr = $(tr);
                let value = String($(tr.find('td')[col_number]).data('dgr-raw-filter-value'));
                if (value.indexOf(filter_by) == -1) {
                    tr.addClass('d-none');
                }
            }
        }
    },
    show_toggler_cols() {
        let template = Handlebars.compile($("#tpl-toggler-cols-modal-panel").html());
        let html = template({columns: this.cols.hiddenable()});
        $(`#toggler-cols-modal-panel`).remove();
        $(document.body).append($(html));
        $(`#toggler-cols-modal-panel`).modal();
        $("#lst-tbl-cols .tbl-col-item input[type=checkbox]").bootstrapToggle();
        this.__hidden_cols.forEach((col_idx, idx)=>{
            $(`#lst-tbl-cols input[type="checkbox"][data-colnumber="${col_idx}"]`).bootstrapToggle('off', true);
        });
    },
    toggle_col(column_indicator) {
        if(column_indicator) {
            let col_idx = column_indicator.data('colnumber');
            let idx = this.__hidden_cols.indexOf(col_idx);
            if(idx > -1) {
                this.__hidden_cols.splice(idx, 1);
                this.__table.find(`tr th:nth-child(${col_idx + 1}), tr td:nth-child(${col_idx + 1})`).removeClass('d-none');
                column_indicator.bootstrapToggle('on',true);
            } else {
                this.__hidden_cols.push(col_idx);
                this.__table.find(`tr th:nth-child(${col_idx + 1}), tr td:nth-child(${col_idx + 1})`).addClass('d-none');
                column_indicator.bootstrapToggle('off',true);
            }
        } else {
            this.__hidden_cols.length = 0;
            this.__table.find(`tr th, tr td`).removeClass('d-none');
            $(`#cntr-extra-actions input[type="checkbox"]`).bootstrapToggle('on', true);
            if($(`.btn-group[aria-label="Filtrado-Filas"]`).hasClass('d-none') && $(`.btn-group[aria-label="Acciones"]`).hasClass('d-none')) {
                this.__table.find('th:nth-child(1), td:nth-child(1)').addClass('d-none');
            }
        }
    },
    __get_selected_record_id(){
        return this.__body.find(`input.massive-operations:checked`).map((idx, element) => $(element).data('dgr-object-id'));
    },
    update_many(){
        let ids = this.__get_selected_record_id();
        if(0 == ids.length) {
            return false;
        }
        location.href = url_update.replace('__recordid__', ids[0]);
    },
    delete_many(){
        let count, ids = this.__get_selected_record_id();
        if(0 == ids.length || !confirm(`Confirma que desea eliminar los elementos seleccionados?`)) {
            return false;
        }
        App.openPanel('Eliminando registros', 'Eliminando...', false);
        for(let id of ids) {
            count++;
            $.get(url_delete.replace('__recordid__', id), () => {
                count--;
                if(!count) {
                    location.reload();
                }
            });
        }
    },
    __sayHi(msg = null) {
        if(msg) {
            console.log(msg);
        } else {
            console.log(`Hola Mundo!!`);
        }
    },
    show_edit_controls() {
        $(`.btn-group[aria-label="Acciones"]`).removeClass('d-none');
        this.__table.find('th:nth-child(1), td:nth-child(1)').removeClass('d-none');
        $("#opc-show-edit-controls").addClass('d-none');
        $("#opc-hide-edit-controls").removeClass('d-none');
    },
    hide_edit_controls() {
        $(`.btn-group[aria-label="Acciones"]`).addClass('d-none');
        this.__table.find('th:nth-child(1), td:nth-child(1)').addClass('d-none');
        $("#opc-show-edit-controls").removeClass('d-none');
        $("#opc-hide-edit-controls").addClass('d-none');
    },
    show_filter_controls() {
        $(`.btn-group[aria-label="Filtrado-Filas"]`).removeClass('d-none');
        this.__table.find('th:nth-child(1), td:nth-child(1)').removeClass('d-none');
        $("#opc-show-filter-controls").addClass('d-none');
        $("#opc-hide-filter-controls").removeClass('d-none');
    },
    hide_filter_controls() {
        $(`.btn-group[aria-label="Filtrado-Filas"]`).addClass('d-none');
        this.__table.find('th:nth-child(1), td:nth-child(1)').addClass('d-none');
        $("#opc-show-filter-controls").removeClass('d-none');
        $("#opc-hide-filter-controls").addClass('d-none');
    },
    filtrar_filas() {
        this.__body.find(`input[type="checkbox"]`).each((idx, input) => {
            let fila = $(input).parent().parent();
            if(input.checked) {
                fila.removeClass('d-none');
            } else {
                fila.addClass('d-none');
            }
        });
    },
    restaurar_filtrado_filas() {
        this.__body.find('tr').removeClass('d-none');
    },
    to_excel() {
        let hoja = $("#main-navbar-title").text().trim().replaceAll(
            regex_nl, " ").replaceAll(regex_spaces, " ");
        let uri = 'data:application/vnd.ms-excel;base64,';
        let base64 = s => window.btoa(unescape(encodeURIComponent(s)));
        let tpl_wbook = Handlebars.compile($("#tpl-to-excel").html());
        let tpl_header = Handlebars.compile($("#tpl-to-excel-header").html());
        let tpl_row = Handlebars.compile($("#tpl-to-excel-row").html());
        let rows = [tpl_header({colums: this.__columns.filter(elem => !elem.cell.hasClass('d-none'))}).trim()];
        this.__body.find('tr').each((idx, tr) => {
            let celdas = $(tr).find('td').filter((idx, cell) => !$(cell).hasClass('d-none'));
            let cells = [];
            celdas.each((idx, celda) => cells.push(celda.innerText));
            rows.push(tpl_row({cells}).trim());
        });
        let html_wbook = tpl_wbook({hoja, rows});
        uri += base64(html_wbook);
        let link = document.createElement('a');
        document.body.appendChild(link);
        link.download = hoja + ".xlsx";
        link.href = uri;
        link.click();
        document.body.removeChild(link);
    },
    to_printer() {
        window.print();
    }
};

dataGridResultsGlobals.init($("#data-grid-report"), true);
