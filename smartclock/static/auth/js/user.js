//	This function will return the current file name
function currentFile() {
	// Step 1: grab the current "location" (URL) of this webpage and put it in a variable
	currentURL = window.location.href;

	// Step 2: find the location (index number) of the last slash (/) in the URL
	fileNameIndex = currentURL.lastIndexOf("/") + 1;

	// Step 3: extract the filename from the URL based on the whatever's to the right of
	//	the last slash
	currentFileName = currentURL.substr(fileNameIndex);
	return currentFileName;
}

username = currentFile();

$('.delete-me').each(function () {
	$(this).on('click', function () {
		if (confirm('Do you really want to delete this account?')) {
			let url = window.origin + "/api/v1/user/" + username;
			$.ajax({
				"url": url,
				"type": "DELETE",
			}).done(function () {
				window.location.replace(window.origin + "/dashboard");
			});
		} else {
			alert('Alright!');
		}
	});
});

$('.approve-me').on('click', function () {
	if (confirm('Do you want to approve this account?')) {
		let url = window.origin + "/api/v1/user/patch/" + username;
		casted_url = String(url); // I don't know what am I doing...
		data_json = {
					"is_approved": true
				}
		$.ajax({
				"url": casted_url,
				"data": JSON.stringify(data_json),
				"dataType": "json",
				"contentType": "application/json",
				"type": "PATCH"
			})
			.done(function () {
				window.location.replace(window.origin + "/dashboard");
			})
			.fail(function (xhr, status, description) {
				alert("There was a problem handling this request");
				console.log("Error: " + description);
				console.log("Status: + status");
			})
			.always(function (xhr, status) {
				console.log("request completed with status code: " + status);
			});

	} else {
		alert('Alright!');
	}
});