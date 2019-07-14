 $(document).ready(function() {
     
     // Removes ingredient / cooking step
     $(document).on("click", "a.remove_ingredient, a.remove_step", function() {
         $(this).closest(".row").remove();
     });
     
     //Adds ingredient
     $(document).on("click", "#add_ingredient", function() {
         var new_ingredient = ` <div class="row" >
                        <div class="name col-10">
                            <div class="control-group">
                                <div class="form-group floating-label-form-group controls">
                                    <label>Name</label>
                                    <input type="text" class="form-control" name="ingredient_name" placeholder="Ingredient Name / Amount" required data-validation-required-message="Please enter name of the ingredient.">
                                    <p class="help-block text-danger"></p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="delete col-1">
                            <a href="javascript:void(0);" class="remove_ingredient"><i class="fas fa-trash-alt red"></i></a>
                        </div>
                    </div>`;
         $(new_ingredient).appendTo("#ingredients");
     });
     
     // Adds cooking step
     $(document).on("click", "#add_step", function() {
         var new_step = ` <div class="row ">
                        <div class="control-group col-10">
                            <div class="form-group floating-label-form-group controls">
                                <label>Step</label>
                                <textarea row="2" class="form-control" placeholder="Step" name="step_name"  required data-validation-required-message="Please enter step."></textarea>
                                <p class="help-block text-danger"></p>
                            </div>
                        </div>
                        <div class="delete col-1">
                            <a href="javascript:void(0);" class="remove_step"><i class="fas fa-trash-alt delete red"></i></a>
                        </div>
                    </div>`
         $(new_step).appendTo("#steps");
     });
     
     //Contact form validation
     $(function() {
         $("input,select,textarea").not("[type=submit]").jqBootstrapValidation();
     });
     
     // Modal is closed automatically after 4s
     $("#alert_modal").modal('show');
     setTimeout(function() {
         $("#alert_modal").modal('hide');
     }, 3500);


 })
 