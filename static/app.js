/**
            An example ajax implementation with the Venmo API.
            This makes a POST request to make a payment on Venmo.
        **/
        function make_payment(venmo_access_token) {
            var num_errors = 0;

            payment_note = $("#payment_note").val();
            if (!payment_note) {
                $("#payment_note_input").addClass("has-error");
                num_errors++;
            } else {
                $("#payment_note_input").removeClass("has-error");
            }

            payment_amount = $("#payment_amount").val();
            if (!payment_amount) {
                $("#payment_amount_input").addClass("has-error");
                num_errors++;
            } else {
                $("#payment_amount_input").removeClass("has-error");
            }

            payment_target = $("#payment_target").val()
            if (!payment_target) {
                $("#payment_target_input").addClass("has-error");
                num_errors++;
            } else {
                $("#payment_amount_input").removeClass("has-error");
            }

            if (num_errors) {
                return;
            }
            post_parameters = {
                note:payment_note,
                amount:payment_amount,
                email:payment_target,
                access_token:venmo_access_token
            }

            $.post("/make_payment",
                    post_parameters).done(function(response) {
                        $("#make_payment_response").text(JSON.stringify(response));
                    }).fail(function(error) {
                        $("#make_payment_response").text(error);
                    });
        };

        /**
            An example ajax implementation with the Venmo API.
            This makes a GET request to get a list of your payments.
        **/
        function get_payments(access_token) {
            url = "/get_payments?access_token=" + access_token;
            $.get(url).done(function(response) {
                $("#get_payments_response").text(JSON.stringify(response));
            }).fail(function(error) {
                $("#get_payments_response").text(error);
            });
        };

        function get_friends(access_token) {
            url = "/get_friends?access_token=" + access_token;
            $.get(url).done(function(response) {
                $("#get_friends_response").text(JSON.stringify(response));
            }).fail(function(error) {
                $("#get_friends_response").text(error);
            });
        };

        function make_group(access_token) {
            group_val = $("#group_raw").val();
            post_parameters = {
                group_raw:group_val
            }
            $.post("/make_group",
                    post_parameters).done(function(response) {
                        $("#make_group_response").text(response);
                    }).fail(function(error) {
                        $("#make_group_response").text(error);
                    });
        };

        function get_groups(access_token) {
            $.get("/get_groups").done(function(response) {
                        $("#get_groups_response").text(response);
                    }).fail(function(error) {
                        $("#get_groups_response").text(error);
                    });
        };

        function make_group_payment(access_token) {
            groupNum = $("#groupNumber").val();
            groupAmt = $("#groupAmt").val();
            groupNote = $("#groupNote").val();            
            groupUsernames = [];
            var row = document.getElementById(groupNum);
            for (i = 0; i < row.cells.length; i++){
                if (row.cells[i].innerHTML != ""){
                    groupUsernames.push(row.cells[i].innerHTML);
                }
            }
            groupCSV = groupUsernames.toString();
            post_parameters = {
                groupUsernames:groupCSV,
                groupAmt:groupAmt,
                groupNote:groupNote
            }
            $.post("/make_group_payment",
                    post_parameters).done(function(response) {
                        $("#make_group_payment_response").text(response);
                    }).fail(function(error) {
                        $("#make_group_payment_response").text(error);
                    });
        };