var index = {

	cur_path: "",
	folder_img_src: "/icon/folder",
	cd_img_src: "/icon/cd",
	play_img_src: "/icon/play",
	file_img_src: "/icon/file",
	shuffle_img_src: "/icon/shuffle",
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
			index.modify_page_num(index.cur_page, index.last_page);
		})
	},

	on_initial: function () {
		this.get_and_display("", 0);
		this.modify_path("")
	},



	create_anchor_element: function (name, type) {
		const anchor_element = $("<div>", {
			class: "anchor-element-div"
		})
	
		const anchor = $("<a>", {
			"name": name,
			class: "content-anchor",
			"href": "javascript: void(0)",
			"content-type": type,
			group: type + "-anchor"
		})

		let source;
		if (type === "directory") {
			source = index.folder_img_src;
		}
		else if (type === "media") {
			source = index.cd_img_src;
		} else {
			source = index.file_img_src;
		}

		const icon = $("<img>", {
			src: source,
			class: "type-icon"
		})

		let group;
		if (type === "directory") {
			group = "directory-play-button"
		} 
		else if (type === "media") {
			group = "media-play-button"
		} else {

		}
		if (type === "directory") {
			source = index.shuffle_img_src;
		} else {
			source = index.play_img_src;
		}
		const play_icon = $("<input>", {
			role: "button",
			type: "image",
			src: source,
			class: "play-button",
			"data-id": index.path_join([index.cur_path, name]),
			"content-type": type,
			group: group
		})

		anchor.html(name);
		anchor_element.append(icon);
		anchor_element.append(anchor);
		
		if (type != "file") {
			anchor_element.append(play_icon)

		}

		return anchor_element;
	},


	handle_back_button_click: function () {
		$("#back-button")[0].onclick = function (e) {
			const cur_path = index.cur_path;
			index.cur_page = 1;
			const path = cur_path.substring(0, cur_path.lastIndexOf("/"));
			//const folder = index.parse_file_name(cur_path);
			index.get_and_display(path, 0);
			index.cur_path = path;
			index.modify_path(index.cur_path);
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
			if (target.getAttribute("content-type") === "directory") {
				const path = encodeURIComponent(index.path_join([index.cur_path, target.name]));
				index.cur_page = 1;
				index.get_and_display(path, 0);
				index.cur_path = index.path_join([index.cur_path, target.name]);
				index.modify_path(index.cur_path);
			}
			if (target.role === "button") {
				
				const path = "/media?path=" + encodeURIComponent(e.target.getAttribute("data-id"));
				/*
				
				*/

				if (target.getAttribute("content-type") === "media") {
					const suffix = /[^.]+$/.exec(path);
					if (suffix[0] === "mp3") {
						$("#music-player-div").removeAttr("hidden");
						$("#mp3-audio").attr("src", path);
						$("#audio-name").html(index.parse_file_name(e.target.getAttribute("data-id")));
						$("#mp3-audio")[0].play()
					}

					if (suffix[0] === "mp4") {
						$("#video-player-div").removeAttr("hidden");
						$("#mp4-video").attr("src", path);
						$("#mp4-video")[0].play();
						$("#video-name").html(index.parse_file_name(e.target.getAttribute("data-id")));
					}
				}
				if (target.getAttribute("content-type") === "directory") {

				}
			}
		}
	},

	handle_music_player_div_click: function () {
		$("#music-player-div")[0].onclick = function (e) {
			const target = e.target;
			if (target.id === "close-music-player-button") {
				$("#mp3-audio")[0].pause()
				$("#music-player-div").attr("hidden", "true")
			}
		}
	},

	handle_video_player_div_click: function () {
		$("#video-player-div")[0].onclick = function (e) {
			const target = e.target;
			if (target.id === "close-video-player-button") {
				$("#mp4-video")[0].pause();
				$("#video-player-div").attr("hidden", "true");
			}
		}
	},

	modify_path: function (path) {
		if (path === "") {
			path = "/"
		}
		$("#path").html(path)
	}
}