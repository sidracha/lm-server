var index = {

	cur_path: "",


	parse_file_name: function (path) {
        const x = path.lastIndexOf('/');
        const name = path.substring(x+1, path.length);
        return name;
	},

	path_join: function (parts, sep){
		const separator = sep || '/';
		parts = parts.map((part, index)=>{
			if (index) {
				part = part.replace(new RegExp('^' + separator), '');
			}
			if (index !== parts.length - 1) {
				part = part.replace(new RegExp(separator + '$'), '');
			}
			return part;
		})
		return parts.join(separator);
	},

	get_all_under: function (folder) {
		const path = encodeURIComponent(this.path_join([this.cur_path, folder]))
		//console.log(path)
		const start_time = Date.now()
		$.ajax({
			url: "/sub?path=" + path,
			method: "GET",
		}).done(function(resp) {
			for (item of resp.contents) {
				//console.log(index.parse_file_name(item))
				const end_time = Date.now()
				console.log(end_time-start_time)
				console.log(item)
			}
		})
	},

	handle_click: function () {
		$("#test")[0].onclick = function (e) {
			index.get_all_under("")
		}
	}

}