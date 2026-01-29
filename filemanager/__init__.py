"""
Copyright © 2024 Walkline Wang (https://walkline.wang)
Gitee: https://github.com/Walkline80/ESP-File_manager
Forked: https://github.com/mispacek/ESP-File_manager
"""
import os


# /www/index.html
index = r'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible"content="IE=edge,chrome=1"><meta name="viewport"content="width=device-width, initial-scale=0.80, maximum-scale=1.0, user-scalable=yes"/><meta name="mobile-web-app-capable"content="yes"><meta name="apple-mobile-web-app-capable"content="yes"><title>MicroPython File Manager</title><link rel="stylesheet"href="styles.css"></head><body><div class="file-manager"><div class="toolbar"><input type="file"id="file-upload"style="display: none;"multiple><button id="upload"><span>上传</span></button><button id="download"><span>下载</span></button><button id="move-to"><span>移动到</span></button><button id="copy-to"><span>复制到</span></button><button id="rename"><span>重命名</span></button><button id="new-folder"><span>新建文件夹</span></button><button id="delete"><span>删除</span></button><button id="clear-selection"><span>清除选择</span></button><button id="reboot"><span>重启设备</span></button></div><div id="breadcrumb-container"><div class="breadcrumb"id="breadcrumb"></div><div id="status-container"><div id="progressbar-container"><div id="progressbar"></div></div><div id="memory-status"></div></div></div><div class="file-list"id="file-list"ondrop="handleDrop(event)"ondragover="allowDrop(event)"><table id="file-table"><thead><tr><th>选择</th><th>文件名</th><th>文件大小</th></tr></thead><tbody><!--Dynamic file listing--></tbody></table></div><div id="error-message"style="color: red;"></div></div><div id="popup-overlay"class="popup-overlay"style="display: none;"><div id="popup-window"class="popup-window"><div id="popup-content"></div><button id="popup-close"class="popup-button">Close</button></div></div><script src="scripts.js"></script></body></html>'''.encode()

# /www/scripts.js
scripts = r'''document.addEventListener('DOMContentLoaded',function(){loadDirectoryContents('/');document.getElementById('upload').addEventListener('click',()=>document.getElementById('file-upload').click());document.getElementById('file-upload').addEventListener('change',handleFileInputChange);document.getElementById('download').addEventListener('click',downloadFiles);document.getElementById('move-to').addEventListener('click',moveTo);document.getElementById('copy-to').addEventListener('click',copyTo);document.getElementById('rename').addEventListener('click',renameFile);document.getElementById('new-folder').addEventListener('click',new_Folder);document.getElementById('delete').addEventListener('click',deleteFiles);document.getElementById('clear-selection').addEventListener('click',clearSelection);document.getElementById('reboot').addEventListener('click',rebootDevice);document.getElementById('popup-close').addEventListener('click',closePopup);updateStatus();setInterval(updateStatus,5000)});let currentPath='/';let selectedFiles=[];let popup_modal=false;let popupTimer;let upIconBase64="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAENklEQVR42p2WTWxUVRTH//fNR9vhTttpSwkfEogulI0L485oEBNTQxNXLmrUkLBS4mfjZ0JABGpAExokJSYS17oBwWAUhbgxGuPGFijETChlOm1npjN905n37nvv+L8zVRfaMOMkkztv3n3nd87/f86dUWjjpceXBSHgvpZWrT7T8kb98Yrs2GqwfUscF65EcN9qDdLSJn3UlcyAwaWRXiQEeP5yBb/9zEre77nr83fdoA+5kkx78s2ejLrHUVgyEeZDhZe/K+PmFCGHMup/A/SBZVHar53f09u1o8vBVDnElCvQCcCJKRy9VEH2moI7tjZkzRt6f1mky8fZvX14SDuYrIT4qUiPlSAIBN1JB/GY4NjFCuazhBzrVy0D9NtlqSc8fLkvg8e647jK4D8WI96hAVx8vmu+oKvDgRBy+mwJ5Vwc7okBdVeAfndJauLhzIsZDK9P4DpluVyIEIg04ptI4IXNdcUHutc5qAYhvriwhOpigpD1ak2AfqcsrqlhYl8fntmQwDQz/34xgm8E4gAhIYbB6wzuB7y2EK69nTGU+cX5r8owtRjc8Q3qXwD9RkmqXh2nXu/Ds5uSyC6HODsfYsUAHdS9vpq1BfirAFqBgJ1VZyW6S6FQDXDlXIkbKNfERvU3QB8uS9L3sP+FHoxsTqJKfacqEX5YCBAyUJzZe6zCBjZWJhvcfubqMoMYDQdBujuBIkv65RwrMZTrk0Gl9AdLIjGDoYeTGHpgHW7OGxQ8QQfbMMXIK+x7L5RGttFqFRbUuOa+/M07rMBBgFQjk9TGJFxKO32pjM5+DaUPlyQW+thEzYvM2mP2QSnCwH0JjO7S2NYJfH0rQMn6YD1gB5nQSsWgJFZuzCE77UXVZAdHIw6nnkCyLw7PDRCY2NpzkDlYkCPP6UabnrzhYYbwuGoaXWf6oePA0Jjq7TkUFjWyBze3Pgf2NfBRUUafSuGRPgenr3uYrQAxZQeN+pumwX6dLbtwC8uzA8iObWwP0D9WkJd2r8NOngKnrhssLFMb26qm2UmBKAR+iFohj5U/Upg5sbU9QO+RRdk7lMLj/TGcvOqhYCvAPx74HIyQAHOnCI+dOXv83vYAmQMLMmIr6HcwMUlAuSnRX7MQRgqGAP92nqtG/sM2K+h5b16eHk5hFyv4dNJHgRIp25p2DihTGNFknhn12TxUoLFwvF3AaF6eZAWPbojhs9/rKC9xszWZ7gZ2HuiBEGBycxBWUBrf3h4g/WpOntjNNt3i4MyvPkpLUfMwtcdDGEFYgW8lyuWRNGmUTm1rD6BfycnO4TQGU4JvJw0CTq1we2Sn2rap4lFtTZ7J0fw03HYBg2/mpP/BFGps/Br1dzi1hlMeBZz2aoiIwUOeXz4d1xxC9/P726xgJCu1QpGyqEb/C7Nm40NFQeNXjYcP7F8YewTpjgG4F/8b8CftPHDwwRULGgAAAABJRU5ErkJggg==";let folderIconBase64="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAADtElEQVR42r1V3WtcRRT/nbvZjd0k/UgqNqIPimiRqrVQQitIkRIp6IOiYBGf/B/6YouKVCzSJimxKSLWmFQJptJigvhJ6YOiD1raICmtSW2bdDfZbJrdfJo7c3rm4969KVZrig53mHvnzpzfOb/fmTOE/7jR/wJwbiexDhngpbBBmvDQJ3xbTtDAi8T1Tz2P+uad4MUFB6IZVFWF4rc9KJ48jg2fLR+EfnkWvL6lFyvubQTm8tY4WIv7hNnhIZx7cxc2nVg+lfTTDvCGd7uRvWcFeK5k3AdCDUqlMD38O357ey+a+m8D4Idm8KMHulHTWA1emLL2oRUoCFA6P4jTe/ajqubvFPzraaoCtvSB6Pvt4M0HulDbmJEIBMCIoA2KgFSvwXwxjXB2CmRkIHYOmJGlK23pZGPSfBvLZhTnpgZP40Lv+6BvtoGb2j5G3bq0AFxzANFmeag6Gxuy8wnD8ZxxiJVQ6/UTesuXLuLntvdAXz4J3traiZWNBmDSR8CWJrvYbFbRN1cMRyDaA+jEdwCURkbx4+Eu0PEt4G3tH2HVupRocM1vhDckMStV8dxSJ2Oo3Ki8Eyq0DrBfE0gGTl4examObtCxJvD29g+x0gBYDQyfsmF+QgCnAQuq3JylTblu5tL1QoeoGUgWZOpkXtaEi5LhhOKVEZzs+BTUsxncfOgIVq/V0JNnxKCALJQTOnh65J0tFRGQ6Yvyy0SwKH6lEWRWg2ruFrw7MXHpMr7rOAo6ugm8o20f1mQvQs8WHd/+LDheQ3kig95zG4V2xg2g+WdoE0BDVxBkMDm3Cl93nQJ1bgQ/0/IW6uuuQk8X4s2x15FBjkBdBFon6EqsN53EqYmxGXzVPwr64BHwc60CUDsCXR7zmXAzSpQ8CYM6Etj9Zx9RIAkwkZ9Df99V0OGHwS+0vYGGmisCkLPscJR2OinsDZQsEdw449aQ6XImCmPzONGXA7WvB7/U+joaav+ALuVtAHG4CQNLKFHJCFTFuAcyERTGF/B5Xx7U8iD4ldY9aMgOQ5XHK4fIR6BjsZXTgBOUJL9j6rRN03EB6PlCAPbfD3754G7clR2CKuXiYucoSYh4U0qUTwSf0tJSctDyBQE4JgDv3Ad+9dBurM0MyfkejfNf61vgOzTvob9DOK6uUoqQy/2Jzl7RYN8D4MeefgKPb7wDaqYgGyjOf1c2uFKTTOUMXemwnrOvUze0VIrw68AMzg6WHeZeiSIM/6HO/5srR9bKjYvXLsh9sNyb6lbbdQUO3sO94PfiAAAAAElFTkSuQmCC";let fileIconBase64="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAEQElEQVR42q2Wa2gcVRTH/3dmNpFo1LW1tQpVsPpBRYKCH3xBNVpFCD4o2BYrPip+KFWUSmuzSKXGVrRYFBGUNLVG66NBQY2SUgVtIKlpikhe3W7DZjfNJrvJZmdn532v585uYrYbog29szNzH7Pzu+f8zz13GOaUd9t+E4IzeD6HEAJgDArkje4MyJocKnVM2yYy2RxiSR2de19gWKCwcwFr77o1qIdCKgqGi5xVQN7yYNguJg0DU7oP03IQHTuLobMZ2CZbEFI2sOebo+LJe+uwclk4aAs6CgUHuuUjZ5rI6XmkDAcutftTaXSc6MOdN16PzqE4fn3rWXZeAN91YcIjgEozdmE5eVhkRYascjlHf2ISA/E41t99C9q6TuOveGpeSFlH06GjYsPqEsD3yQQOByosy4JpFKCbPrlLwPFdDCTS6IrGEFn/IHzHw57vOtE/Ml4BKWvsaj0inqq/rQRwIAVnigLLJ0tMFwXbg+OIwHm9sQR6h9N4e+N9SE7pGBweR3tvFD2x0TJIGeDNL46Ip++fAVjgXJWBBEGnSZFlkNie40MRPs6M5/Bjz+kAMJ3LI+8LxJNjaOuO4afjA+j7+GVWAYh83iGef+D2WQs4Lw7LEPVLECmwdJFBWnScHArGdV0gL5yg/uepUZxJjmPwk1cqAVubfxabH7ljVgNOYs48xEoQuUZytoDnOsVAsDhp5GIsa6CmRsOJ6Aj2/dCN4eatlYAtH34vXl17TwDwCOAQoKo0JkoPC9JkmqLJcVxwl7SREUagdNbCZZdWo+tUArsP/Y6Rz16rBGza2yoaNzxctADSFRzShhBdtDnPeb4Cm9swPBt2nsEVFgFMrLgijGODcfJEO0YPbqsErGtqEbufawgABs1OkAV0RTUljBD5yKc6p1RRJeseie6RBTb1ei4mcgWsWnEl/uiL45l9h5Fq3V4JaIh8Kj7Y/HgAyBgWVC6Cl2rkFpUpxXAinykqWUSC+HSa3IVHwk/oBm6+dhmO/T2Cx5oOYuLLHZWA1TuaRcuWRwPAZL4QOD6I+kBshhA5qppgjhQmBFwkgR4ja0mDnIkbrg7jZHQU9Y37kfmq8f8B5hbZVCmdqlIRjRXB9AsRdIIsXrnkYgrTBNY0HsDk14sBULuqSoNLM1YVjVyngVM6UVgxnSwJ16B7KIGHIgcwtRgAAgtUiiIC0BEiMaSXpAMdSidLay8A4N8cw0orEMGmZHIfV9VeguMEWHMhAHLWMoRZIL5MIz6uubx2YcBNL74v2ndunAWweQDyD5xE9SWCQlSlhaFpGkxKgsvDZEFJ5P8EpKZ1WqHFfuUciGlTIqTcxlSaP0WVRgtvqmCh7rrl6IkmUb99P7LfRioBS594Q/R89NLslrmYIveGuk3vIX14ZyWgtuF10d+ybdEvnymr1u2C9cs78wPk3RXSKeK8Xio/cxjlr5kyA/gHM7+cN0oReEMAAAAASUVORK5CYII=";function updateStatus(){fetch('/status').then(response=>response.json()).then(data=>{updateProgressBar(data.progress);updateMemoryStatus(data.memoryFree,data.memoryTotal)}).catch(error=>{console.error('Error fetching status:',error)})}function updateProgressBar(progress){const progressBar=document.getElementById('progressbar');progressBar.style.width=progress+'%';progressBar.style.backgroundColor=`hsl(${120-(120*progress)/100},75%,62%)`}function updateMemoryStatus(free,total){const memoryStatus=document.getElementById('memory-status');memoryStatus.textContent=`${free}MB/${total}MB`}function allowDrop(event){event.preventDefault()}function handleDrop(event){event.preventDefault();let items=event.dataTransfer.items;if(items.length>0){handleItems(items)}}function handleFileInputChange(event){let files=event.target.files;let fileArray=[];for(let i=0;i<files.length;i++){fileArray.push(files[i])}if(fileArray.length>0){processFilesAndDirs(fileArray,currentPath)}}function handleItems(items){let entryPromises=[];for(let i=0;i<items.length;i++){let item=items[i].webkitGetAsEntry();if(item){entryPromises.push(processEntry(item,currentPath))}}Promise.all(entryPromises).then(()=>{loadDirectoryContents(currentPath);showNotification("Upload completed successfully!")}).catch((error)=>{showError("Upload failed: "+error.message)})}function processFilesAndDirs(files,path){let directoryStructure={};for(let file of files){let relativePath=file.webkitRelativePath||file.name;let pathParts=relativePath.split('/');let currentLevel=directoryStructure;for(let i=0;i<pathParts.length;i++){if(i===pathParts.length-1){if(!currentLevel._files){currentLevel._files=[]}currentLevel._files.push(file)}else{if(!currentLevel[pathParts[i]]){currentLevel[pathParts[i]]={}}currentLevel=currentLevel[pathParts[i]]}}}processDirectoryStructure(directoryStructure,path).then(()=>{loadDirectoryContents(currentPath);showNotification("Upload completed successfully!")}).catch((error)=>{showError("Upload failed: "+error.message)})}function processDirectoryStructure(structure,path){let promises=[];for(let key in structure){if(key==='_files'){for(let file of structure._files){promises.push(uploadFileToServer(file,path+'/'+file.name))}}else{let newPath=path+'/'+key;promises.push(createDirectory(newPath).then(()=>{return processDirectoryStructure(structure[key],newPath)}))}}return Promise.all(promises)}function processEntry(entry,path){return new Promise((resolve,reject)=>{if(entry.isFile){entry.file(file=>{uploadFileToServer(file,path+'/'+file.name).then(resolve).catch(reject)})}else if(entry.isDirectory){let newPath=path+'/'+entry.name;createDirectory(newPath).then(()=>{let dirReader=entry.createReader();readAllDirectoryEntries(dirReader).then(entries=>{let subEntryPromises=entries.map(subEntry=>processEntry(subEntry,newPath));Promise.all(subEntryPromises).then(resolve).catch(reject)})}).catch(reject)}})}function readAllDirectoryEntries(dirReader){let entries=[];return new Promise((resolve,reject)=>{function readEntries(){dirReader.readEntries((results)=>{if(results.length){entries=entries.concat(results);readEntries()}else{resolve(entries)}},reject)}readEntries()})}function createDirectory(path){return fetch(`/newfolder?data=${JSON.stringify({foldername:path})}`,{method:'POST'}).then(response=>{if(response.ok){showNotification("Directory "+path+" created successfully!");return response.text()}else{showError("Directory "+path+" upload failed!");throw new Error('Failed to create directory');}})}function uploadFileToServer(file,path){return new Promise((resolve,reject)=>{showNotification(" Uploading "+file.name+" Please wait... ");const reader=new FileReader();reader.onload=function(event){const fileSize=event.target.result.byteLength;const hexData=hexEncode(event.target.result);const xhr=new XMLHttpRequest();xhr.open("POST",`/upload;${path};${fileSize}`,true);xhr.setRequestHeader("Content-Type","text/plain");xhr.onreadystatechange=function(){if(xhr.readyState===XMLHttpRequest.DONE){if(xhr.status===200){showNotification("File "+file.name+" uploaded successfully!");resolve()}else{showError("Upload "+file.name+" failed!");reject(new Error("Upload "+file.name+" failed"))}}};xhr.send(hexData)};reader.readAsArrayBuffer(file)})}function hexEncode(buffer){const byteArray=new Uint8Array(buffer);return Array.from(byteArray,byte=>('0'+(byte&0xFF).toString(16)).slice(-2)).join('')}function resetPopupTimer(){clearTimeout(popupTimer);popupTimer=setTimeout(closePopup,8000)}function showPopup(content){document.getElementById('popup-content').innerHTML=content;document.getElementById('popup-overlay').style.display='flex';resetPopupTimer()}function closePopup(){document.getElementById('popup-overlay').style.display='none';popup_modal=false;clearTimeout(popupTimer)}function showError(message){popup_modal=true;document.getElementById('popup-close').style.display='block';showPopup('<p style="color: red;">'+message+'</p>')}function showNotification(message){popup_modal=true;document.getElementById('popup-close').style.display='block';showPopup('<p style="color: green;">'+message+'</p>')}function showLoading(message){popup_modal=false;document.getElementById('popup-close').style.display='none';showPopup('<p style="color: black;">'+message+'</p>')}function downloadAll(urls){var link=document.createElement('a');link.setAttribute('download',null);link.style.display='none';document.body.appendChild(link);for(var i=0;i<urls.length;i++){link.setAttribute('href',urls[i]);link.click()}document.body.removeChild(link)}function loadDirectoryContents(path){currentPath=path;updateBreadcrumb();console.log("Updating file list");if(document.getElementById('popup-overlay').style.display=='none'){showLoading("  Loading...  ")}fetch('/contents?path='+currentPath).then(response=>response.json()).then(data=>{const fileTable=document.getElementById('file-table').querySelector('tbody');fileTable.innerHTML='';if(path!=='/'){const row=document.createElement('tr');const selectCell=document.createElement('td');const nameCell=document.createElement('td');nameCell.style.cursor='pointer';nameCell.addEventListener('click',()=>loadDirectoryContents(path.substring(0,path.lastIndexOf('/'))||'/'));nameCell.innerHTML=`<img src="${upIconBase64}"class="file-icon">..`;const sizeCell=document.createElement('td');sizeCell.textContent='';row.appendChild(selectCell);row.appendChild(nameCell);row.appendChild(sizeCell);fileTable.appendChild(row)}const directories=data.contents.filter(file=>file.isDirectory).sort((a,b)=>a.name.localeCompare(b.name));const files=data.contents.filter(file=>!file.isDirectory).sort((a,b)=>a.name.localeCompare(b.name));const sortedContents=directories.concat(files);sortedContents.forEach(file=>{const row=document.createElement('tr');const selectCell=document.createElement('td');const selectInput=document.createElement('input');selectInput.type='checkbox';selectInput.addEventListener('change',()=>{if(selectInput.checked){selectedFiles.push(file.path)}else{selectedFiles=selectedFiles.filter(f=>f!==file.path)}});selectCell.appendChild(selectInput);const nameCell=document.createElement('td');const iconSrc=file.isDirectory?folderIconBase64:fileIconBase64;const icon=document.createElement('img');icon.className='file-icon';icon.src=iconSrc;nameCell.appendChild(icon);nameCell.appendChild(document.createTextNode(file.name));if(file.isDirectory){nameCell.style.cursor='pointer';nameCell.addEventListener('click',()=>loadDirectoryContents(file.path))}const sizeCell=document.createElement('td');sizeCell.textContent=file.isDirectory?'-':`${file.size}`;row.appendChild(selectCell);row.appendChild(nameCell);row.appendChild(sizeCell);fileTable.appendChild(row)});if(popup_modal==false){closePopup()}}).catch(error=>{showError(error.message)})}function updateBreadcrumb(){const breadcrumb=document.getElementById('breadcrumb');breadcrumb.innerHTML='';const pathParts=currentPath.split('/').filter(part=>part);const link=document.createElement('a');link.href='javascript:loadDirectoryContents("/");';link.textContent="\u00A0\u00A0/\u00A0\u00A0\u00A0";breadcrumb.appendChild(link);let path='';pathParts.forEach((part,index)=>{path+=`/${part}`;const link=document.createElement('a');link.href='javascript:loadDirectoryContents("'+path+'");';link.textContent=part;breadcrumb.appendChild(link);if(index<pathParts.length-1){breadcrumb.appendChild(document.createTextNode(' / '))}})}function downloadFiles(){let files=[];selectedFiles.forEach(file=>{files.push(`/download?path=${file}`)});downloadAll(files);clearSelection()}function moveTo(){const destination=prompt('Enter destination path:\n\nExamples:\nPath from root: \u00A0\u00A0\u00A0\u00A0 /Folder\nRelative path: \u00A0\u00A0\u00A0\u00A0 folder1/folder2');if(destination){showLoading("  Moving files...  ");fetch(`/move?data=${JSON.stringify({src:selectedFiles,dest:destination})}`,{method:'POST'}).then(function(response){if(response.ok){showNotification("Files moved successfully!");return response.text()}throw new Error('Something went wrong.');}).then(function(text){loadDirectoryContents(currentPath);clearSelection();showNotification("Files moved successfully!")}).catch(function(error){showError('Server error: '+error)})}}function new_Folder(){const folder_name=prompt('Enter new folder name:');let new_path=currentPath+'/'+folder_name;new_path=new_path.replace(/\/\//g,'/');if(folder_name){fetch(`/newfolder?data=${JSON.stringify({foldername:new_path})}`,{method:'POST'}).then(function(response){if(response.ok){return response.text()}throw new Error('Something went wrong.');}).then(function(text){loadDirectoryContents(currentPath);clearSelection();showPopup('Directory created successfully!')}).catch(function(error){showError('Server error: '+error)})}}function copyTo(){const destination=prompt('Enter destination path:\n\nExamples:\nPath from root: \u00A0\u00A0\u00A0\u00A0 /Folder\nRelative path: \u00A0\u00A0\u00A0\u00A0 folder1/folder2');if(destination){showLoading("  Copying files...  ");fetch(`/copy?data=${JSON.stringify({src:selectedFiles,dest:destination})}`,{method:'POST'}).then(function(response){if(response.ok){showNotification("Files copied successfully!");return response.text()}throw new Error('Something went wrong.');}).then(function(text){loadDirectoryContents(currentPath);clearSelection();showNotification("Files copied successfully!")}).catch(function(error){showError('Server error: '+error)})}}function renameFile(){if(selectedFiles.length!==1){alert('Please select exactly one file to rename.');return}const newName=prompt('Enter new name:',selectedFiles[0].split('/').pop());let new_path=currentPath+'/'+newName;new_path=new_path.replace(/\/\//g,'/');if(newName){showLoading("  Renaming files...  ");fetch(`/rename?data=${JSON.stringify({old_name:selectedFiles[0],new_name:new_path})}`,{method:'POST'}).then(function(response){if(response.ok){return response.text()}throw new Error('Something went wrong.');}).then(function(text){loadDirectoryContents(currentPath);clearSelection();showPopup('File renamed successfully!')}).catch(function(error){showError('Server error: '+error)})}}function deleteFiles(){showLoading("  Deleting files...  ");fetch(`/delete?files=${JSON.stringify(selectedFiles)}`,{method:'DELETE'}).then(function(response){if(response.ok){return response.text()}throw new Error('Something went wrong.');}).then(function(text){loadDirectoryContents(currentPath);clearSelection();showPopup('Files deleted successfully!')}).catch(function(error){showError('Server error: '+error)})}function clearSelection(){selectedFiles=[];document.querySelectorAll('#file-table input[type="checkbox"]').forEach(checkbox=>checkbox.checked=false)}function rebootDevice(){showLoading("  Rebooting device...  ");fetch('/reboot')}'''.encode()

# /www/styles.css
styles = r'''body{font-family:Arial,sans-serif;background-color:#f5f5f5;margin:0;padding:0}.file-manager{max-width:1200px;margin:auto;margin-top:10px;border:1px solid #ddd;border-radius:10px;background-color:#fff;box-shadow:0 0 10px rgba(0,0,0,0.1);overflow:hidden}.toolbar{display:flex;gap:10px;padding:6px;background-color:#f0f0f0;color:white;position:relative;max-width:1200px;top:0;z-index:1000}.toolbar button{padding:10px 15px;border:none;border-radius:5px;background-color:#a0a0a0;color:white;cursor:pointer;font-size:16px}.toolbar button:hover{background-color:#808080}.toolbar button img.icon{width:16px;height:16px;margin-right:5px;vertical-align:middle}.breadcrumb{margin-top:0px;padding:10px;font-size:18px}.breadcrumb a{text-decoration:none;color:#007bff;margin-right:5px}.breadcrumb a:hover{text-decoration:underline}.file-list{margin:10px;border:1px solid #ddd;border-radius:5px;overflow:auto;max-height:calc(100vh - 140px)}#file-table{width:100%;border-collapse:collapse}#file-table tr{border-bottom:1px solid #ddd}#file-table tr:last-child{border-bottom:none}#file-table tr:hover{background-color:#ddd}#file-table th,#file-table td{padding:10px;text-align:left}#file-table th{background-color:#f0f0f0}.file-icon{width:20px;height:20px;margin-right:10px;vertical-align:middle}#error-message{margin-top:10px;color:red}@media (max-width:750px){.toolbar button{padding:15px}.toolbar button span{display:none}.toolbar button img.icon{margin-right:0}}.popup-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.2);display:flex;justify-content:center;align-items:center;z-index:2000}.popup-window{background:white;border-radius:10px;padding:20px;box-shadow:0 0 10px rgba(0,0,0,0.2);max-width:90%;max-height:90%;overflow-y:auto}.popup-button{margin-top:20px;padding:10px 20px;background-color:#a0a0a0;color:white;border:none;border-radius:5px;cursor:pointer}.popup-button:hover{background-color:#808080}#breadcrumb-container{display:flex;align-items:center;justify-content:space-between}#status-container{display:flex;align-items:center;margin-right:10px}#progressbar-container{width:100px;height:20px;background-color:#ddd;border-radius:5px;overflow:hidden;margin-right:10px}#progressbar{height:100%;width:0;background-color:red;border-radius:5px;transition:width 1s,background-color 1s}#memory-status{font-size:14px;color:#333}'''.encode()

# main.py
init = r'''import gc
from micropython import alloc_emergency_exception_buf

module_folder = ''
__version__ = '0.0.3'

try:
	from utilities import connect_to_wifi
	from web_server import WebServer
	from web_handler import *
except ImportError:
	from .utilities import connect_to_wifi
	from .web_server import WebServer
	from .web_handler import *

	module_folder = 'filemanager'


alloc_emergency_exception_buf(128)
gc.collect()

# Start WWW serveru
webserver = WebServer(web_folder=f'/{module_folder}/www', port=8080)

#region Handlers for web_handlers
@webserver.handle('/contents')
def _handle_contents(client, path, request):
	handle_contents(client, path, request)

@webserver.handle('/upload')
def _handle_upload(client, path, request):
	handle_upload(client, path, request)

@webserver.handle('/download')
def _handle_download(client, path, request):
	handle_download(client, path, request)

@webserver.handle('/delete')
def _handle_delete(client, path, request):
	handle_delete(client, path, request)

@webserver.handle('/rename')
def _handle_rename(client, path, request):
	handle_rename(client, path, request)

@webserver.handle('/newfolder')
def _handle_newfolder(client, path, request):
	handle_newfolder(client, path, request)

@webserver.handle('/move')
def _handle_move(client, path, request):
	handle_move(client, path, request)

@webserver.handle('/copy')
def _handle_copy(client, path, request):
	handle_copy(client, path, request)

@webserver.handle('/status')
def _handle_status(client, path, request):
	handle_status(client, path, request)

@webserver.handle('/reboot')
def _handle_reboot(client, path, request):
	handle_reboot(client, path, request)
#endregion

if connect_to_wifi():
	webserver.start()
	gc.collect()
'''.encode()

# web_handler.py
web_handler = r'''"""
Copyright © 2024 Walkline Wang (https://walkline.wang)
Github: https://github.com/Walkline80/ESP-File_manager
Forked: https://github.com/mispacek/ESP-File_manager
"""
import os
import json
import socket
import binascii

try:
	from utilities import (
		is_directory,
		read_in_chunks,
		convert_file_size,
		file_path_exists,
	)
except ImportError:
	from .utilities import (
	is_directory,
	read_in_chunks,
	convert_file_size,
	file_path_exists,
)


FM_500 = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\n"
FM_200_JSON = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
FM_200_TEXT = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"

def urldecode(str: str):
	dic = {"%21":"!","%22":'"',"%23":"#","%24":"$","%26":"&","%27":"'","%28":"(","%29":")","%2A":"*","%2B":"+","%2C":",","%2F":"/","%3A":":","%3B":";","%3D":"=","%3F":"?","%40":"@","%5B":"[","%5D":"]","%7B":"{","%7D":"}"}
	for k,v in dic.items(): str=str.replace(k,v)
	return str

def parse_query_string(query_string: str):
	query = query_string.split('?')[1]
	params = query.split('&')
	param_dict = {}

	for param in params:
		key, value = param.split('=')
		param_dict[key] = value
	
	return param_dict

def list_directory_contents(base_path: str):
	contents = []

	try:
		for entry in os.listdir(base_path):
			if base_path == '/':
				entry_path = '/' + entry
			else:
				entry_path = base_path + '/' + entry
			
			#print(entry_path)
			
			if is_directory(entry_path):
				contents.append({
					'name': entry,
					'path': entry_path,
					'isDirectory': True
				})
			else:
				contents.append({
					'name': entry,
					'path': entry_path,
					'isDirectory': False,
					'size': convert_file_size(os.stat(entry_path)[6])
				})
	except OSError as e:
		print("OSError:", e)

	return contents

def delete_path(path: str):
	if not file_path_exists(path):
		return

	stack = [path]

	while stack:
		current_path = stack.pop()

		if is_directory(current_path):
			try:
				entries = list(os.ilistdir(current_path))
				if not entries:
					# Directory is empty, we can delete it
					os.rmdir(current_path)
				else:
					# Add directory back to stack to try again later
					stack.append(current_path)
					# Add entries to stack
					for entry in entries:
						entry_path = current_path + '/' + entry[0]
						stack.append(entry_path)
			except Exception as e:
				print(f"Error accessing directory {current_path}: {e}")
		else:
			try:
				os.remove(current_path)
			except Exception as e:
				print(f"Error deleting file {current_path}: {e}")


#region handlers
def handle_contents(client: socket.socket, path: str, request):
	try:
		query_params = path.split('?path=')[1] if '?path=' in path else '/'
		full_path = query_params
		
		contents = list_directory_contents(full_path)
		response = json.dumps({"contents": contents})
		client.send(FM_200_JSON)
		client.sendall(response)
	except Exception as e:
		print("Error:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_upload(client: socket.socket, path: str, request):
	try:
		_, filepath, filesize = path.split(';')
		filesize = int(filesize) * 2
		data_read = 0

		with open(filepath, 'wb') as file:
			data = request[request.find(b'\r\n\r\n') + 4:]

			if data:
				data_read = len(data)

				if data_read % 2 == 0:
					file.write(binascii.unhexlify(data))
				else:
					data = data + client.read(1)
					file.write(binascii.unhexlify(data))

				data_read = len(data)

			while data_read < filesize:
				try:
					chunk_size = min(1024, filesize - data_read)
					chunk = client.read(chunk_size)
					file.write(binascii.unhexlify(chunk))
					data_read = data_read + chunk_size
					percentage = (data_read / filesize) * 100
					#print(f"{percentage:.1f}%")

					if not chunk:
						break
				except OSError as e:
					if e.args[0] == 116:  # ETIMEDOUT
						break
					else:
						raise e

		#print("File Saved")
		client.send(FM_200_TEXT)
		client.send("Upload successful")
	except Exception as e:
		print("Error during file upload:", e)
		client.send(FM_500)
		client.send("Upload failed")

def handle_download(client: socket.socket, path: str, request):
	try:
		file_path = urldecode(path).split('?path=')[1]
		file_name = file_path.split('/')[-1]

		if file_path_exists(file_path):
			client.send(f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Disposition: attachment; filename=\"{file_name}\"\r\nContent-Length: {os.stat(file_path)[6]}\r\n\r\n")
			with open(file_path, 'rb') as f:
				for piece in read_in_chunks(f):
					client.write(piece)
		else:
			client.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n")
			client.send("File not found.")
	except OSError as e:
		print("OSError:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_delete(client: socket.socket, path: str, request):
	try:
		files = json.loads(urldecode(path).split('?files=')[1])

		for file_path in files:
			delete_path(file_path) 

		client.send(FM_200_TEXT)
		client.send("Files deleted successfully.")
	except OSError as e:
		print("OSError:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_rename(client: socket.socket, path: str, request):
	try:
		query_params = json.loads(urldecode(path).split('?data=')[1])
		old_name = query_params['old_name']
		new_name = query_params['new_name']
		os.rename(old_name, new_name)
		client.send(FM_200_TEXT)
		client.send("File renamed successfully.")
	except OSError as e:
		print("OSError:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_newfolder(client: socket.socket, path: str, request):
	try:
		query_params = json.loads(urldecode(path).split('?data=')[1])
		folderpath = query_params['foldername']
		os.mkdir(folderpath)
		client.send(FM_200_TEXT)
		client.send("New folder created successfully.")
	except OSError as e:
		print("OSError:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_copy(client: socket.socket, path: str, request):
	try:
		query_params = json.loads(urldecode(path).split('?data=')[1])
		src_files = query_params['src']
		dest_path = query_params['dest']
		stack = []

		for src in src_files:
			stack.append((src, dest_path))

		while stack:
			current_src, current_dest = stack.pop()
			if is_directory(current_src):
				new_dir_path = current_dest + '/' + current_src.split('/')[-1]
				os.mkdir(new_dir_path)

				for entry in os.listdir(current_src):
					stack.append((current_src + '/' + entry, new_dir_path))
			else:
				with open(current_src, 'rb') as f_src:
					with open(current_dest + '/' + current_src.split('/')[-1], 'wb') as f_dest:
						for piece in read_in_chunks(f_src):
							f_dest.write(piece)

		client.send(FM_200_TEXT)
		client.send("Files copied successfully.")
	except OSError as e:
		print("OSError:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_move(client: socket.socket, path: str, request):
	try:
		query_params = json.loads(urldecode(path).split('?data=')[1])
		src_files = query_params['src']
		dest_path = query_params['dest']
		stack = []

		for src in src_files:
			stack.append((src, dest_path))

		# Přesun souborů a adresářů
		while stack:
			current_src, current_dest = stack.pop()
			if is_directory(current_src):
				new_dir_path = current_dest + '/' + current_src.split('/')[-1]

				if not file_path_exists(new_dir_path):
					os.mkdir(new_dir_path)

				for entry in os.listdir(current_src):
					stack.append((current_src + '/' + entry, new_dir_path))
			else:
				os.rename(current_src, current_dest + '/' + current_src.split('/')[-1])

		# Smazání prázdných původních adresářů
		for src in src_files:
			delete_path(src)

		client.send(FM_200_TEXT)
		client.send("Files moved successfully.")
	except OSError as e:
		print("OSError:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_status(client: socket.socket, path: str, request):
	try:
		s = os.statvfs('//')
		flash_total = (s[0] * s[2]) / 1024 ** 2
		flash_used = flash_total - (s[0] * s[3]) / 1024 ** 2
		usage_percent = flash_used / flash_total * 100

		contents = ({
			'progress': '{0:.1f}'.format(usage_percent),
			'memoryFree': '{0:.1f}'.format(flash_used),
			'memoryTotal': '{0:.1f}'.format(flash_total)
		})

		response = json.dumps(contents)
		client.send(FM_200_JSON)
		client.sendall(response)
	except Exception as e:
		print("Error:", e)
		client.send(FM_500)
		client.send("Internal Server Error")

def handle_reboot(client: socket.socket, path: str, request):
	import machine
	machine.reset()
#endregion
'''.encode()

# utilities.py
utilities = r'''"""
Copyright © 2024 Walkline Wang (https://walkline.wang)
Gitee: https://github.com/Walkline80/ESP-File_manager
Forked: https://github.com/mispacek/ESP-File_manager
"""
import os
import network
from time import sleep_ms


def file_path_exists(path: str) -> bool:
	try:
		os.stat(path)
		return True
	except OSError:
		return False

def is_directory(path: str) -> bool:
	try:
		return os.stat(path)[0] & 0x4000 != 0
	except OSError:
		return False

def read_in_chunks(file_object, chunk_size: int = 1024):
	while True:
		data = file_object.read(chunk_size)

		if not data:
			break

		yield data

def convert_file_size(size: int) -> str:
	units = 'Bytes', 'KB', 'MB', 'GB', 'TB'
	unit = units[0]

	for i in range(1, len(units)):
		if size >= 1024:
			size /= 1024
			unit = units[i]
		else:
			break

	return f'{size:.2f} {unit}'

def connect_to_wifi() -> bool:
	sta = network.WLAN(network.STA_IF)
	sta.active(True)

	if sta.isconnected():
		return True

	wifi_list = sta.scan()

	print('Wifi List:')
	for index, wifi in enumerate(wifi_list, start=1):
		print(f'    [{index}] {wifi[0].decode()}')

	selected = None
	while True:
		try:
			selected = int(input('Choose a wifi to connect: '))
			assert isinstance(selected, int) and 0 < selected <= len(wifi_list)
			break
		except KeyboardInterrupt:
			return False
		except:
			pass

	ssid = wifi_list[selected - 1][0].decode()
	password = input(f'Input password for {ssid}: ')

	sta.connect(ssid, password)

	while (not sta.isconnected()):
		status = sta.status()

		if status in [network.STAT_IDLE, network.STAT_GOT_IP, network.STAT_NO_AP_FOUND, network.STAT_WRONG_PASSWORD]:
			break
		elif status == network.STAT_CONNECTING:
			pass

		sleep_ms(200)

	sleep_ms(1000)
	status = sta.status()

	if status == network.STAT_GOT_IP:
		print("Wifi connected, network config:", sta.ifconfig())
		return True
	else:
		print(f'Connect wifi failed with status code: {status}')
		return False
'''.encode()

# web_server.py
web_server = r'''"""
Copyright © 2024 Walkline Wang (https://walkline.wang)
Github: https://github.com/Walkline80/ESP-File_manager
Forked: https://github.com/mispacek/ESP-File_manager
"""
import network
import socket
import _thread

try:
	from utilities import (
		file_path_exists,
		read_in_chunks,
	)
except ImportError:
	from .utilities import (
		file_path_exists,
		read_in_chunks,
	)


class WebServer:
	MIMETYPES = {
		"txt"   : "text/plain",
		"htm"   : "text/html",
		"html"  : "text/html",
		"css"   : "text/css",
		"csv"   : "text/csv",
		"js"    : "application/javascript",
		"xml"   : "application/xml",
		"xhtml" : "application/xhtml+xml",
		"json"  : "application/json",
		"zip"   : "application/zip",
		"pdf"   : "application/pdf",
		"ts"    : "application/typescript",
		"ttf"   : "font/ttf",
		"jpg"   : "image/jpeg",
		"jpeg"  : "image/jpeg",
		"png"   : "image/png",
		"gif"   : "image/gif",
		"svg"   : "image/svg+xml",
		"ico"   : "image/x-icon",
		"cur"   : "application/octet-stream",
		"tar"   : "application/tar",
		"tar.gz": "application/tar+gzip",
		"gz"    : "application/gzip",
		"mp3"   : "audio/mpeg",
		"wav"   : "audio/wav",
		"ogg"   : "audio/ogg"
	}

	def __init__(self, web_folder: str = '/www', port: int = 80):
		self.__web_folder = web_folder
		self.__webserv_sock = None
		self.__url_handlers = {}
		self.__port = port

	def get_mime_type(self, filename: str):
		try:
			_, ext = filename.rsplit(".", 1)
			return self.MIMETYPES.get(ext, "application/octet-stream")
		except:
			return "application/octet-stream"

	def serve_file(self, client: socket.socket, path: str):
		try:
			if path.startswith("/*GET_FILE"):
				file_path = path.replace("/*GET_FILE", "")
			else:
				if path == "/":
					path = "/index.html"

				file_path = self.__web_folder + path

			mime_type = self.get_mime_type(file_path)
			filestatus = 0 # 0=Not found  1=Found  2=found in GZip

			if file_path_exists(file_path + '.gz'):
				filestatus = 2
				file_path += '.gz'
			elif file_path_exists(file_path):
				filestatus = 1

			if filestatus > 0:
				with open(file_path, 'rb') as file:
					client.write(b'HTTP/1.1 200 OK\r\n')
					client.write(b"Content-Type: " + mime_type.encode() + b"\r\n")

					if filestatus == 2:
						client.write(b'Content-Encoding: gzip\r\n')

					client.write(b'\r\n')

					for piece in read_in_chunks(file):
						client.write(piece)
			else:
				client.write(b"HTTP/1.0 404 Not Found\r\n\r\nFile not found.")
		except OSError as e:
			print("OSError:", e)
			client.write(b"HTTP/1.0 500 Internal Server Error\r\n\r\nInternal error.")
		except Exception as e:
			print("Exception:", e)
			client.write(b"HTTP/1.0 500 Internal Server Error\r\n\r\nInternal error.")

	def handle(self, pattern):
		"""Decorator to register a handler for a specific URL pattern."""
		def decorator(func):
			self.__url_handlers[pattern] = func
			return func

		return decorator

	def client_handler(self, client: socket.socket):
		try:
			request = client.recv(2048)

			if request:
				_, path, _ = request.decode("utf-8").split(" ", 2)

				for pattern, handler in self.__url_handlers.items():
					if path.startswith(pattern):
						try:
							handler(client, path, request)
						except Exception as e:
							print("Handler Exception:", e)
						client.close()

						return
				# Default file serving if no handler matches
				self.serve_file(client, path)
		except Exception as e:
			#print("Webserver Exception:", e)
			pass
		finally:
			client.close()

	def web_thread(self):
		while True:
			try:
				cl, _ = self.__webserv_sock.accept()
				cl.settimeout(2)  # time in seconds
				self.client_handler(cl)
			except Exception as e:
				#print("Webserver Exception:", e)
				pass

	def start(self):
		addr = socket.getaddrinfo('0.0.0.0', self.__port)[0][-1]
		self.__webserv_sock = socket.socket()
		self.__webserv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__webserv_sock.bind(addr)
		self.__webserv_sock.listen(5)

		_thread.start_new_thread(self.web_thread, ())

		for interface in [network.AP_IF, network.STA_IF]:
			wlan = network.WLAN(interface)

			if not wlan.active():
				continue

			ifconfig = wlan.ifconfig()
			print(f"Web server running at: http://{ifconfig[0]}:{self.__port}")

	def stop(self):
		if self.__webserv_sock:
			self.__webserv_sock.close()
'''.encode()

file_list = {
	'www/index.html': index,
	'www/scripts.js': scripts,
	'www/styles.css': styles,
	'__init__.py': init,
	'web_handler.py': web_handler,
	'utilities.py': utilities,
	'web_server.py': web_server
}

module_folder = '/filemanager'

def install():
	def mkdir(path: str):
		try:
			os.mkdir(path)
		except OSError:
			pass

	def mkdirs(paths: list):
		cwd = module_folder

		for folder in paths:
			cwd += '/' + folder
			mkdir(cwd)

	mkdir(module_folder)

	for file, content in file_list.items():
		mkdirs(file.split('/')[:-1])

		with open(f'{module_folder}/{file}', 'wb') as output:
			output.write(content)

	import sys
	sys.modules.pop('filemanager')
	import filemanager

install()
