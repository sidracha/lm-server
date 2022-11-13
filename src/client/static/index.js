var index = {

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
	cur_id: "root",
	prev_ids: [],


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

	get_and_display: function (id, offset) {
		$.ajax({
			url: "/sub?id=" + id + "&limit=" + index.limit + "&offset=" + offset,
			method: "GET",
		}).done(function(resp) {
			$(".anchor-element-div").remove();
			index.total = resp.total;
			index.last_page = Math.ceil(resp.total/index.limit);
			for (item of resp.contents) {
				const anchor_element = index.create_anchor_element(item.name, item.type, item.id);
				anchor_element.prependTo($("#contents-div"));
			}
			index.modify_page_num(index.cur_page, index.last_page);
		})
	},

	on_initial: function () {
		this.get_and_display("root", 0);
		this.modify_path("")
	},



	create_anchor_element: function (name, type, id) {
		const anchor_element = $("<div>", {
			class: "anchor-element-div"
		})
	
		const anchor = $("<a>", {
			"name": name,
			class: "content-anchor",
			"href": "javascript: void(0)",
			"content-type": type,
			group: type + "-anchor",
			"data-id": id
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
			"data-id": id,
			"content-type": type,
			"name": name
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
			if (index.prev_ids.length === 0) {
				return;
			}
			const id = index.prev_ids.pop();
			console.log(index.prev_ids);
			index.go_to_page(id, 1);
			index.cur_id = id;
			const path = $("#path").html();
			index.modify_path(path.substring(0, path.lastIndexOf("/")))
		}
		
	},

	go_to_page: function (id, page) {
		const offset = (page-1) * index.limit;
		this.get_and_display(id, offset)
		index.cur_page = page
	},

	handle_next_page_button_click: function () {
		$("#next-page-button")[0].onclick = function () {
			const last_page = Math.ceil(index.total/index.limit);
			if (index.cur_page === last_page) {
				return;
			}
			index.go_to_page(index.cur_id, index.cur_page+1);
			
		}
		
	},

	handle_previous_page_button_click: function() {
		$("#previous-page-button")[0].onclick = function () {
			if (index.cur_page === 1) {
				return;
			}

			index.go_to_page(index.cur_id, index.cur_page-1);
			
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
				const id = target.getAttribute("data-id");
				index.prev_ids.push(index.cur_id)
				index.cur_id = id;
				index.go_to_page(id, 1);
				const path = index.path_join([$("#path").html(), target.getAttribute("name")]);
				index.modify_path(path);
			}
			if (target.role === "button") {
				
				const id = target.getAttribute("data-id")
				const name = target.getAttribute("name")

				if (target.getAttribute("content-type") === "media") {

					const suffix = /[^.]+$/.exec(name);
					const source = "/media/" + id

 					if (suffix[0] === "mp3") {
						$("#music-player-div").removeAttr("hidden");
						$("#mp3-audio").attr("src", source);
						$("#audio-name").html(name);
						$("#mp3-audio")[0].play()
					}

					if (suffix[0] === "mp4") {
						$("#video-player-div").removeAttr("hidden");
						$("#mp4-video").attr("src", source);
						$("#mp4-video")[0].play();
						$("#video-name").html(name);
					}
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
			$("#path").html("/");
			return;
		}
		$("#path").html(path)
	}
}