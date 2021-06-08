$("#myForm").validate({
  // Specify validation rules
  rules: {
    email_id: {
      required: true,
      //   email: true
    },
    password: {
      required: true,
      minlength: 8,
      maxlength: 20,
    },
  },
  // Specify validation error messages
  messages: {
    password: {
      required: "Please provide a password",
      minlength: "Your password must be at least 8 characters long",
    },
    email_id: "Please enter a valid email address",
  },
  // Make sure the form is submitted to the destination defined
  // in the "action" attribute of the form when valid
});

$("#registrationForm").validate({
    // Specify validation rules
    rules: {
      fname: { required: true},
      mname: { required: true},  
      lname: { required: true},
      email_id: {
        required: true,
        //   email: true
      },
      password: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      bdate: {
        required: true,
      },
      adhaar:{
          required: true,
          minlength: 12,
          maxlength: 12
      },
      add:{
        required: true
      },
      city: {required: true},
      state: {required: true},
      country: {required: true},
      phone: {
          required: true,
          minlength: 10,
          maxlength: 10
      },
      pincode: {
          required: true,
          minlength: 6,
          maxlength: 6
      },
      cpassword:{
        required: true,
        minlength: 8,
        maxlength: 20,
        equalTo: password
      },
    },
    // Specify validation error messages
    messages: {
        fname: { required: "Enter First name"}, 
        mname: { required: "Enter Middle name"}, 
        lname: { required: "Enter Last name"}, 
        password: {
            required: "Please provide a password",
            minlength: "Your password must be at least 8 characters long",
        },
        cpassword: {
            equalTo: "Confirm password must be same as password"  
        },
        email_id: "Please enter a valid email address",
        phone:{
            minlength: "please enter 10 digit number",
            maxlength: "please enter 10 digit number",
        },
        adhaar: {
            minlength: "please enter 12 digit aadharcard number",
            maxlength: "please enter 12 digit aadharcard number",
        },
        pincode: {
            minlength: "please enter 6 digit pincode number",
            maxlength: "please enter 6 digit pincode number",
        }
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
  });