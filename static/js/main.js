$(document).ready(function () {
  $(function () {
    $("#plist")
      .DataTable({
        responsive: true,
        lengthChange: false,
        autoWidth: false,
        ordering: true,
        searching: true,
        info: false,
        buttons: ["print"],
        lengthMenu: [5],
        positionMenu: "center",
      }).buttons().container().appendTo('#plist_wrapper .col-md-6:eq(0)');
    
  });

  // select2 supplier dropdwon
  $("#id_supplier").select2();
  $("#id_supplier").on("select2:open", function (e) {
    $("#select2-id_supplier-results").change(function () {
      var data = $(this).val();
      // alert(data);
      $("").val(data);
    });
  });

  // select2 add Stook dropdwon
  $("#id_category").select2();
  $("#id_category").on("select2:open", function (e) {
    $("#id_category").change(function () {
      var data = $(this).val();
      //  alert(data);
    });
  });

  // select2 add Stook dropdwon
  $("#id_product").select2();
  $("#id_product").on("select2:open", function (e) {
    $("#id_product").change(function () {
      var data = $(this).val();
      //  alert(data);
    });
  });

  // select2 add Stook dropdwon
  $("#id_stock").select2();
  $("#id_stock").on("select2:open", function (e) {
    $("#id_stock").change(function () {
      var data = $(this).val();
      //  alert(data);
    });
  });

  //  alert
  //   setTimeout(function () {
  //     $(".invalid-feedback").fadeOut();
  //     $(".is-invalid").addClass("remove-error");
  //   },15000)

  //   // }, 20200);
  // $(".is-invalid").on('focus',function () {
  //     $(this).addClass("remove-error");
  //   // $(".invalid-feedback").fadeOut();
  //       // $(".is-invalid").addClass("remove-error");

  // });

  //  alert
  setTimeout(function () {
    $(".alert").fadeOut();
  }, 6000);

  // Purchses Form
  //updates the total price by multiplying 'price per item' and 'quantity'
  $(document).on("change", ".setprice", function (e) {
    e.preventDefault();
    //gets the values
    var element = $(this);
    var quantity = element.parents(".form-row").find(".quantity").val();
    var perprice = element.parents(".form-row").find(".price").val();
    //calculates the total
    var tprice1 = quantity * perprice;

    // converts price to kenyan currenxy
    var formatter = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "ksh",
    });
    var tprice = formatter.format(tprice1);

    //sets it to field
    element.parents(".form-row").find(".totalprice").val(tprice);
    return false;
  });


  $("#carr").each(function () {
    var item = $(this).text();
    var num = Number(item).toLocaleString("en");

    if (Number(item) < 0) {
      num = num.replace("-", "");
      $(this).addClass("negMoney");
    } else {
      $(this).addClass("enMoney");
    }

    $(this).text(num);
  });

  $("#carr2").each(function () {
    var item = $(this).text();
    var num = Number(item).toLocaleString("en");

    if (Number(item) < 0) {
      num = num.replace("-", "");
      $(this).addClass("negMoney");
    } else {
      $(this).addClass("enMoney");
    }

    $(this).text(num);
  });
  // counter
  $(".disp").each(function () {
    $(this)
      .prop("Counter", 0)
      .animate(
        {
          Counter: $(this).text(),
        },
        {
          duration: 1000,
          easing: "swing",
          step: function (now) {
            $(this).text(Math.ceil(now));
          },
        }
      );
  });



        
        
        //stores the total no of item forms
        var total = 1;

        function cloneMore(selector, prefix) {
            var newElement = $(selector).clone(true);
            //var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
            newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
                var name = $(this).attr('name')
                if(name) {
                    name = name.replace('-' + (total-1) + '-', '-' + total + '-');
                    var id = 'id_' + name;
                    $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
                }
            });
            newElement.find('label').each(function() {
                var forValue = $(this).attr('for');
                if (forValue) {
                forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
                $(this).attr({'for': forValue});
                }
            });
            total++;
            $('#id_' + prefix + '-TOTAL_FORMS').val(total);
            $(selector).after(newElement);
            return false;
        }
        
        // form deletion 
        function updateElementIndex(el, prefix, ndx) {
          var id_regex = new RegExp('(' + prefix + '-\\d+)');
          var replacement = prefix + '-' + ndx;
          if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
          if (el.id) el.id = el.id.replace(id_regex, replacement);
          if (el.name) el.name = el.name.replace(id_regex, replacement);
      }
        function deleteForm(prefix, btn) {
            //var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
            if (total > 1){
                btn.closest('.form-row').remove();
                var forms = $('.form-row');
                $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
                for (var i=0, formCount=forms.length; i<formCount; i++) {
                    $(forms.get(i)).find(':input').each(function() {
                        updateElementIndex(this, prefix, i);
                    });
                }
                total--;
            } else {
              Swal.fire({
                title: 'Error!',
                text: "This field cannot be deleted!",
                icon: 'warning',
                width: 400,
                showCancelButton: true,
                showConfirmButton:false,
                cancelButtonColor: '#d33',
              }
              )
            }
            return false;
        }
        
        $(document).on('click', '.add-form-row', function(e){
            e.preventDefault();
            cloneMore('.form-row:last', 'form');
            return false;
        });
        
        $(document).on('click', '.remove-form-row', function(e){
            e.preventDefault();
            deleteForm('form', $(this));
            return false;
        });


        //updates the total price by multiplying 'price per item' and 'quantity' 
        $(document).on('change', '.setprice', function(e){
            e.preventDefault();
            //gets the values
            var element = $(this);
            var quantity = element.parents('.form-row').find('.quantity').val();
            var perprice = element.parents('.form-row').find('.price').val();
            //calculates the total
            var tprice = quantity * perprice;
            //sets it to field
            element.parents('.form-row').find('.totalprice').val(tprice);
            return false;
        });

});
