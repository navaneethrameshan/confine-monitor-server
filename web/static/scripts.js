jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "file-size-pre": function ( a ) {

        if(a.substr(0, 2) == "<a") {
            a = jQuery(a).text();
            var x = a.substring(0,a.length - 1);
        } else {
            var x = a.substring(0,a.length - 1);
        }


        var x_unit =
            (a.substring(a.length - 1, a.length) == "B" ? 10 :
                (a.substring(a.length - 1, a.length) == "K" ? 10000  :
                    (a.substring(a.length - 1, a.length) == "M" ? 10000000 :
                        (a.substring(a.length - 1, a.length) == "G" ? 10000000000 : 1))));

        if(isNaN(x)) {
            return -1;
        } else {
            return parseInt( x * x_unit, 10 );
        }
    },

    "file-size-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "file-size-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
} );