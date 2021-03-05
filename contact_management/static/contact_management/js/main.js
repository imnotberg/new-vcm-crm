
const user_input = $("#user-input")
const search_icon = $('#search-icon')
const artists_div = $('#replaceable-content')
const endpoint = '/artists/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out the artists_div, then:
			artists_div.fadeTo('slow', 0).promise().then(() => {
				// replace the HTML contents
				artists_div.html(response['html_from_view'])
				// fade-in the div with new contents
				artists_div.fadeTo('slow', 1)
				// stop animating search icon
				search_icon.removeClass('blink')
			})
		})
}


user_input.on('keyup', function () {

	const request_parameters = {
		q: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// start animating the search icon with the CSS class
	search_icon.addClass('blink')

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
function getData(){
	console.log('getting data!')
}
document.addEventListener("DOMContentLoaded", getData);

function populateContactDataTable(data) {
	 	$('#contacts-list-table').DataTable().clear();
	    console.log("populating conta data table...");    
	    var contacts = data.contacts;
	    console.log('contacts' + contacts);
	    $('#search-card-body').remove();
	    $('#search-card').append(`<div class="card" id="search-card-body"><div class="card-body"><div class="card-title">contacts</div><div class="table-responsive"><table class="table table-sm table-hover" id="main-contacts-list-table"><thead><tr><th>Name</th><th>Account</th><th>City</th><th>State</th><th>Phone</th><th>Email</th></tr></thead></table></div></div></div>`);

	    // clear the table before populating it with more data
	    $('#main-contacts-list-table').DataTable();
	    //$("#contacts-list-table").DataTable();
	    var length = Object.keys(data.contacts).length;
	    for(var i = 0; i < contacts.length; i++) {
	      var contact = contacts[i];
	      // You could also use an ajax property on the data table initialization
	     $('#main-contacts-list-table').DataTable().row.add( [
	        contact["full_name"],
	        contact["account_name"],
	        contact["city"],
	        contact["state"],
	        contact["phone"],
	        contact["email"],


	      ]).draw();
	    }
	  }
