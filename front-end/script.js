// script.js

const url = 'http://localhost:8000/api/contacts/'

window.getTasks = async function (skip = 0, limit = 10) {
  const response = await fetch(`${url}?offset=${skip}&limit=${limit}`)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const contacts = await response.json()
  return contacts
}

window.createTask = async function (task) {
  const response = await fetch(`${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(task),
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.editTask = async function (task) {
  const response = await fetch(`${url}${contacts.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(task),
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}

window.deleteTask = async function (id) {
  const response = await fetch(`${url}${id}`, {
    method: 'DELETE',
  })
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
}
