var index = {

	cur_path: "",
	folder_img_src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqmgjXGGj5Z4775Va8mU9e7wWN8LviQQudbm3CvAU&s",
	cd_img_src: "data:image/jpeg;base64,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",
	play_img_src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrB7udWCFpOg7BOrgcdf7ZJ9ndv4Uz9OOxuJ8hC0A&s",
	file_img_src: "https://www.iconpacks.net/icons/2/free-file-icon-1453-thumb.png",
	limit: 20,
	offset: 0,
	cur_page: 1,
	total: 0,
	last_page: 0,

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

	get_and_display: function (path, offset) {
		//console.log(path);
		$.ajax({
			url: "/sub?path=" + path + "&limit=" + index.limit + "&offset=" + offset,
			method: "GET",
		}).done(function(resp) {
			index.total = resp.total
			index.last_page = Math.ceil(resp.total/index.limit)
			$(".anchor-element-div").remove()
			let count = 0
			for (item of resp.contents) {
				//console.log(item)
				const anchor_element = index.create_anchor_element(item.name, item.type);
				anchor_element.prependTo($("#contents-div"));
				count++;
			}
			index.count = count;
			index.modify_page_num(index.cur_page, index.last_page)
		})
	},

	on_initial: function () {
		this.get_and_display("", 0);
	},



	create_anchor_element: function (name, type) {
		const anchor_element = $("<div>", {
			class: "anchor-element-div"
		})
		const anchor = $("<a>", {
			"name": name,
			"class": "content",
			"href": "javascript: void(0)",
			"type": type
		})
		let source;
		let ismedia = false;
		if (type === "directory") {
			source = index.folder_img_src;
		}
		if (type === "file") {
			source = index.file_img_src;
		}
		if (type === "mp3") {
			source = index.cd_img_src;
			ismedia = true
		}

		const icon = $("<img>", {
			src: source,
			class: "type-icon"
		})

		anchor.html(name);
		anchor_element.append(icon);
		anchor_element.append(anchor);
		if (ismedia) {
			const play_icon = $("<input>", {
				class: "play-button",
				role: "button",
				type: "image",
				src: index.play_img_src,
				"data-id": index.path_join([index.cur_path, name])
			})
			anchor_element.append(play_icon)
		}
		return anchor_element;
	},

	display_contents: function (contents) { // contents comes in a list of objects
		let content;
		for (content of contents) {
			if (content.type === "file") {
				continue;
			}

			const anchor_element = this.create_anchor_element(content.name);
			anchor_element.prependTo($("$contents-div"))

		}
	},
	/*
	handle_anchor_click: function () {
		$("#contents-div")[0].onclick = function (e) {
			const target = e.target;
			if (target.type != "directory") {
				return
			}
			const path = encodeURIComponent(index.path_join([index.cur_path, target.name]));
			index.get_and_display(path, 0)
			index.cur_path = index.path_join([index.cur_path, target.name])
		}
	},
	*/

	handle_back_button_click: function () {
		$("#back-button")[0].onclick = function (e) {
			const cur_path = index.cur_path;
			const path = cur_path.substring(0, cur_path.lastIndexOf("/"));
			const folder = index.parse_file_name(cur_path);
			index.get_and_display(path, 0);
			index.cur_path = path;
		}
		
	},

	go_to_page: function (page) {
		const offset = (page-1) * index.limit;
		this.get_and_display(this.cur_path, offset)

	},

	handle_next_page_button_click: function () {
		$("#next-page-button")[0].onclick = function () {
			const last_page = Math.ceil(index.total/index.limit);
			index.max_page = last_page
			if (index.cur_page === last_page) {
				return;
			}
			index.cur_page += 1;
			index.go_to_page(index.cur_page);
			
		}
		
	},

	handle_previous_page_button_click: function() {
		$("#previous-page-button")[0].onclick = function () {
			if (index.cur_page === 1) {
				return;
			}
			index.cur_page -= 1;
			index.go_to_page(index.cur_page);
			
		}
	
	},
	
	modify_page_num: function (cur, last) {
		if (last === 0) {last = 1}
		$("#page-num").html(cur + " of " + last)
	},

	handle_contents_div_click: function () {
		$("#contents-div")[0].onclick = function (e) {
			const target = e.target;
			if (target.type === "directory") {
				const path = encodeURIComponent(index.path_join([index.cur_path, target.name]));
				index.get_and_display(path, 0);
				index.cur_path = index.path_join([index.cur_path, target.name]);
			}
			if (target.role === "button") {
				const path = "/mp3?path=" + encodeURIComponent(e.target.getAttribute("data-id"));
				$("#music-player-div").removeAttr("hidden");
				$("#mp3-audio").attr("src", path);
				$("#audio-name").html(index.parse_file_name(e.target.getAttribute("data-id")));
				$("#mp3-audio")[0].play()
			}
		}
	}
}