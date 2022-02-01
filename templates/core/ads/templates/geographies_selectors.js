

// Handling the province -> municipality dropdown dependencies
$(function(){ 
    // inspect html to check id of category select dropdown.
    $(document).on('change', "select#id_province", function(){ 
        $.getJSON("/ajax/load-municipalities/",{province: $(this).val()}, function(j){ 
            var options = '<option value="">---------</option>'; 
            for (var i = 0; i < j.length; i++) { 
                options += '<option value="' + j[i].id + '">' + j[i].name + '</option>'; 
            } 
            // inspect html to check id of subcategory select dropdown.
            $("select#id_municipality").html(options); 

            // Reset areas field 
            var empty_options = '<option value="">---------</option>';
            $("select#id_area").html(empty_options);  

        }); 
    }); 
}); 

// Handling the municipality -> areas dropdown dependencies 
$(function(){ 
    // inspect html to check id of category select dropdown.
    $(document).on('change', "select#id_municipality", function(){ 
        $.getJSON("/ajax/load-areas/",{municipality: $(this).val()}, function(j){ 
             var options = '<option value="">---------</option>'; 
             for (var i = 0; i < j.length; i++) { 
                options += '<option value="' + j[i].id + '">' + j[i].name + '</option>'; 
             } 
             // inspect html to check id of subcategory select dropdown.
             $("select#id_area").html(options); 
         }); 
     }); 
 }); 
