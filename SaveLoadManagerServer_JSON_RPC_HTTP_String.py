#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ^\s*(?=\r?$)\n
html_string = ('''
<!-- SaveLoadManagerServer_JSON_RPC_HTTP.html -->
<!-- ^\s*(?=\r?$)\n -->
<!DOCTYPE html>
<html>

<head>
    <title>JSON-RPC Frontend</title>
    <link rel="shortcut icon" href="#" />
    <link rel="shortcut icon" href="data:,">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        .container {
            margin: auto;
            width: 90%;
        }

        .container label {
            width: 25%;
            display: inline-block;
            text-align: right;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }

        .container input {
            width: 69%;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }

        .container select {
            width: 71.5%;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }

        .container button {
            width: 32%;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }

        .class_dialog label {
            width: 30%;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }

        .class_dialog input {
            width: 55%;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }

        .class_dialog button {
            width: 30%;
            padding: 2% 0.5%;
            margin: 0.6% 0.1%;
        }
    </style>
</head>

<body>
    <!-- Simple modal dialog containing a form -->
    <dialog class="class_dialog" id="dialog">
        <form method="dialog">
            <p>
                <label id="dialog_label"></label>
                <input id="dialog_input" type="text"><br>
            </p>
            <div>
                <button value="">Cancel</button>
                <button id="dialog_confirmBtn">Confirm</button>
            </div>
        </form>
    </dialog>
    <div class="container">
        <button id="button_game_delete">Delete Game</button>
        <button id="button_profile_new">New Profile</button>
        <button id="button_profile_delete">Delete Profile</button><br>
        <button id="button_save_new">Save</button>
        <button id="button_save_delete">Delete</button>
        <button id="button_save_load">Load</button><br>
        <label>Game:</label>
        <select id="select_game"></select><br>
        <label>Folder:</label>
        <input id="input_folder" type="text" readonly><br>
        <label>File:</label>
        <input id="input_file" type="text" readonly><br>
        <label>Profile:</label>
        <select id="select_profile"></select><br>
        <label>Comment:</label>
        <input id="input_comment" type="text"><br>
        <label>Save:</label>
        <select id="select_save"></select><br>
    </div>
    <output></output>
    <script>
        window.addEventListener("load", async (event) => {
            await game_list_init();
            await profile_list_init();
            await save_list_init_without_comment();
        });
        // If a browser doesn't support the dialog, then hide the
        // dialog contents by default.
        if (typeof document.getElementById("dialog").showModal !== "function") {
            document.getElementById("dialog").hidden = true;
            /* a fallback script to allow this dialog/form to function
               for legacy browsers that do not support <dialog>
               could be provided here.
            */
        }
        // "Favorite animal" input sets the value of the submit button
        document.getElementById("dialog").querySelector("#dialog_confirmBtn").addEventListener("click", () => {
            document.getElementById("dialog").querySelector("#dialog_confirmBtn").value = document.getElementById("dialog_input").value;
        })
        var button_current = "";
        // "Update details" button opens the <dialog> modally
        document.getElementById("button_game_delete").addEventListener("click", () => {
            if (typeof document.getElementById("dialog").showModal === "function") {
                button_current = "button_game_delete";
                document.getElementById("dialog_label").textContent = "Delete Game: ";
                document.getElementById("dialog_input").readOnly = true;
                document.getElementById("dialog_input").value = document.getElementById("select_game").value;
                document.getElementById("dialog").showModal();
            } else {
                document.querySelector("output").value = "Sorry, the <dialog> API is not supported by this browser.";
            }
        })
        // "Update details" button opens the <dialog> modally
        document.getElementById("button_profile_new").addEventListener("click", () => {
            if (typeof document.getElementById("dialog").showModal === "function") {
                button_current = "button_profile_new"
                document.getElementById("dialog_label").textContent = "New Profile: "
                document.getElementById("dialog_input").readOnly = false
                document.getElementById("dialog_input").value = ""
                document.getElementById("dialog").showModal();
            } else {
                document.querySelector("output").value = "Sorry, the <dialog> API is not supported by this browser.";
            }
        })
        // "Update details" button opens the <dialog> modally
        document.getElementById("button_profile_delete").addEventListener("click", () => {
            if (typeof document.getElementById("dialog").showModal === "function") {
                button_current = "button_profile_delete";
                document.getElementById("dialog_label").textContent = "Delete Profile: ";
                document.getElementById("dialog_input").readOnly = true;
                document.getElementById("dialog_input").value = document.getElementById("select_profile").value
                document.getElementById("dialog").showModal();
            } else {
                document.querySelector("output").value = "Sorry, the <dialog> API is not supported by this browser.";
            }
        })
        // "Update details" button opens the <dialog> modally
        document.getElementById("button_save_delete").addEventListener("click", () => {
            if (typeof document.getElementById("dialog").showModal === "function") {
                button_current = "button_save_delete";
                document.getElementById("dialog_label").textContent = "Delete Save: ";
                document.getElementById("dialog_input").readOnly = true;
                document.getElementById("dialog_input").value = document.getElementById("select_save").value
                document.getElementById("dialog").showModal();
            } else {
                document.querySelector("output").value = "Sorry, the <dialog> API is not supported by this browser.";
            }
        })
        // "Confirm" button of form triggers "close" on dialog because of [method="dialog"]
        document.getElementById("dialog").addEventListener("close", async () => {
            const result = document.getElementById("dialog").returnValue
            if (button_current == "button_game_delete") {
                button_current = "";
                const game = result
                const requestData = {
                    jsonrpc: '2.0',
                    method: 'game_delete',
                    params: [game],
                    id: 0
                };
                const response = await fetch(`/jsonrpc`, {
                    method: 'POST',
                    body: JSON.stringify(requestData)
                });
                const responseData = await response.json();
                document.querySelector("output").value = `Result: ${responseData.result}`;
                await game_list_init();
                await profile_list_init();
                await save_list_init_without_comment();
            }
            if (button_current == "button_profile_new") {
                button_current = "";
                const game = document.getElementById("select_game").value
                const profile = result
                const requestData = {
                    jsonrpc: '2.0',
                    method: 'profile_new',
                    params: [game, profile],
                    id: 0
                };
                const response = await fetch(`/jsonrpc`, {
                    method: 'POST',
                    body: JSON.stringify(requestData)
                });
                const responseData = await response.json();
                document.querySelector("output").value = `Result: ${responseData.result}`;
                await profile_list_init();
                const select_array = Array.from(document.getElementById("select_profile").options).map(obj => obj.value);
                document.getElementById("select_profile")[select_array.indexOf(profile)].selected = true;
                await save_list_init_without_comment();
            }
            if (button_current == "button_profile_delete") {
                button_current = "";
                const game = document.getElementById("select_game").value;
                const profile = result;
                const requestData = {
                    jsonrpc: '2.0',
                    method: 'profile_delete',
                    params: [game, profile],
                    id: 0
                };
                const response = await fetch(`/jsonrpc`, {
                    method: 'POST',
                    body: JSON.stringify(requestData)
                });
                const responseData = await response.json();
                document.querySelector("output").value = `Result: ${responseData.result}`;
                await profile_list_init();
                await save_list_init_without_comment();
            }
            if (button_current == "button_save_delete") {
                button_current = "";
                const save = result
                await save_delete(save);
                await save_list_init_with_comment();
            }
        });
        async function save_delete(save) {
            const game = document.getElementById("select_game").value;
            const profile = document.getElementById("select_profile").value;
            const folder = document.getElementById("input_folder").value;
            const file = document.getElementById("input_file").value;
            const requestData = {
                jsonrpc: '2.0',
                method: 'save_delete',
                params: [game, profile, save, folder, file],
                id: 0
            };
            const response = await fetch(`/jsonrpc`, {
                method: 'POST',
                body: JSON.stringify(requestData)
            });
            const responseData = await response.json();
            document.querySelector("output").value = `Result: ${responseData.result}`;
        }
        async function game_list_func() {
            const requestData = {
                jsonrpc: '2.0',
                method: 'game_list_func',
                params: [],
                id: 0
            };
            const response = await fetch(`/jsonrpc`, {
                method: 'POST',
                body: JSON.stringify(requestData)
            });
            const responseData = await response.json();
            const responseJSON = await JSON.parse(responseData.result);
            return responseJSON;
        }
        async function game_list_init() {
            const data = await game_list_func();
            const game_list = data.game_list;
            var select = document.getElementById('select_game');
            select.options.length = 0;
            for (let game of game_list) {
                var opt = document.createElement('option');
                opt.value = game;
                opt.innerHTML = game;
                select.appendChild(opt);
            }
            select[0].selected = true;
        }
        async function profile_list_func(game) {
            const requestData = {
                jsonrpc: '2.0',
                method: 'profile_list_func',
                params: [game],
                id: 0
            };
            const response = await fetch(`/jsonrpc`, {
                method: 'POST',
                body: JSON.stringify(requestData)
            });
            const responseData = await response.json();
            const responseJSON = await JSON.parse(responseData.result);
            return responseJSON;
        }
        async function profile_list_init() {
            const data = await profile_list_func(document.getElementById('select_game').value);
            const profile_list = data.profile_list;
            const folder = data.folder;
            const file = data.file;
            var select = document.getElementById('select_profile');
            select.options.length = 0;
            for (let profile of profile_list) {
                var opt = document.createElement('option');
                opt.value = profile;
                opt.innerHTML = profile;
                select.appendChild(opt);
            }
            select[0].selected = true;
            document.getElementById('input_folder').value = folder;
            document.getElementById('input_file').value = file;
        }
        async function save_list_func(game, profile) {
            const requestData = {
                jsonrpc: '2.0',
                method: 'save_list_func',
                params: [game, profile],
                id: 0
            };
            const response = await fetch(`/jsonrpc`, {
                method: 'POST',
                body: JSON.stringify(requestData)
            });
            const responseData = await response.json();
            const responseJSON = await JSON.parse(responseData.result);
            return responseJSON;
        }
        async function save_list_init_without_comment() {
            const data = await save_list_func(document.getElementById('select_game').value, document.getElementById('select_profile').value);
            const save_list = data.save_list
            var select = document.getElementById('select_save');
            select.options.length = 0;
            for (let save of save_list) {
                var opt = document.createElement('option');
                opt.value = save;
                opt.innerHTML = save;
                select.appendChild(opt);
            }
            select[0].selected = true;
            await input_comment_init()
        }
        async function save_list_init_with_comment() {
            const data = await save_list_func(document.getElementById('select_game').value, document.getElementById('select_profile').value);
            var save_list = data.save_list
            var save_list_without_comment = data.save_list.filter(obj => { if (obj.indexOf("@") == -1) return obj })
            var save_list_with_comment = data.save_list.filter(obj => { if (obj.indexOf("@") != -1) return obj })
            if (document.getElementById('input_folder').value != "") {
                var save_list_with_same_comment = save_list_with_comment.filter(obj => { if (document.getElementById('input_comment').value == obj.slice(obj.indexOf("@") + 1)) { return obj } })
            } else {
                var save_list_with_same_comment = save_list_with_comment.filter(obj => { if (document.getElementById('input_comment').value == obj.slice(obj.indexOf("@") + 1, obj.lastIndexOf("."))) { return obj } })
            }
            for (let obj of save_list_with_same_comment.slice(3)) {
                await save_delete(obj);
                save_list = save_list.filter(save => { if (save != obj) { return save } })
            }
            for (let obj of save_list_without_comment.slice(3)) {
                await save_delete(obj);
                save_list = save_list.filter(save => { if (save != obj) { return save } })
            }
            var select = document.getElementById('select_save');
            select.options.length = 0;
            for (let save of save_list) {
                var opt = document.createElement('option');
                opt.value = save;
                opt.innerHTML = save;
                select.appendChild(opt);
            }
            if (document.getElementById('input_comment').value == "" && save_list_without_comment.length > 0) {
                select[save_list.indexOf(save_list_without_comment[0])].selected = true;
            } else if (document.getElementById('input_comment').value != "" && save_list_with_same_comment.length > 0) {
                select[save_list.indexOf(save_list_with_same_comment[0])].selected = true;
            } else {
                select[0].selected = true;
            }
            await input_comment_init()
        }
        async function input_comment_init() {
            const var_save = document.getElementById('select_save').value
            if (var_save.indexOf("@") == -1) {
                document.getElementById('input_comment').value = ""
                return
            }
            if (document.getElementById('input_folder').value != "") {
                document.getElementById('input_comment').value = var_save.slice(var_save.indexOf("@") + 1)
            }
            if (document.getElementById('input_file').value != "") {
                document.getElementById('input_comment').value = var_save.slice(var_save.indexOf("@") + 1, var_save.lastIndexOf("."))
            }
        }
        document.getElementById('select_game').addEventListener('change', async () => {
            await profile_list_init();
            await save_list_init_without_comment();
        });
        document.getElementById('select_profile').addEventListener('change', async () => {
            await save_list_init_without_comment();
        });
        document.getElementById('select_save').addEventListener('change', async () => {
            await input_comment_init();
        });
        document.getElementById('button_save_new').addEventListener('click', async () => {
            const game = document.getElementById("select_game").value;
            const profile = document.getElementById("select_profile").value;
            const folder = document.getElementById("input_folder").value;
            const file = document.getElementById("input_file").value;
            const comment = document.getElementById("input_comment").value;
            const requestData = {
                jsonrpc: '2.0',
                method: 'save_new',
                params: [game, profile, folder, file, comment],
                id: 0
            };
            const response = await fetch(`/jsonrpc`, {
                method: 'POST',
                body: JSON.stringify(requestData)
            });
            const responseData = await response.json();
            document.querySelector("output").value = `Result: ${responseData.result}`;
            await save_list_init_with_comment();
        });
        document.getElementById('button_save_load').addEventListener('click', async () => {
            const game = document.getElementById("select_game").value;
            const profile = document.getElementById("select_profile").value;
            const save = document.getElementById("select_save").value;
            const folder = document.getElementById("input_folder").value;
            const file = document.getElementById("input_file").value;
            const requestData = {
                jsonrpc: '2.0',
                method: 'save_load',
                params: [game, profile, save, folder, file],
                id: 0
            };
            const response = await fetch(`/jsonrpc`, {
                method: 'POST',
                body: JSON.stringify(requestData)
            });
            const responseData = await response.json();
            document.querySelector("output").value = `Result: ${responseData.result}`;
        });
    </script>

</html>
</body>
''')