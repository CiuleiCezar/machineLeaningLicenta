const io = require("socket.io")(8900, {
    cors: {
        origin: "http://localhost:7001",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});

const ioWeb = require("socket.io")(8901, {
    cors: {
        origin: "http://localhost:7001",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});

let users = [];

const addUser = (userId, socketId) => {
    console.log(userId, socketId, 'adaugat')
    !users.some(user => user.userId === userId) &&
        users.push({ userId, socketId })
}

const removeUser = (socketId) => {
    users = users.filter(user => user.socketId != socketId)
}

const getUser = (userId) => {
    return users.find(user => user.userId === userId)
}

io.on('connection', (socket) => {
    //when connect
    console.log('user connected', socket.id)

    socket.on("addUser", userId => {
        console.log(userId, socket.id, 'userAdded')

        addUser(userId, socket.id)
        io.emit("getUsers", users)
    })

    //send and get message

    socket.on("sendMessage", ({ senderId, receiverId, text }) => {
        console.log(receiverId)
        const user = getUser(receiverId);
        console.log(users)
        io.to(user?.socketId).emit("getMessage", {
            senderId,
            text
        })
    })

    socket.on("sendNotification", ({receiverId, text}) => {
        console.log(receiverId, text)
        console.log(getUser(receiverId))
        const user = getUser(receiverId)
        io.to(user?.socketId).emit("getNotification", {
            receiverId,
            text
        })
    })

    //when disconnet
    socket.on("disconnect", () => {
        console.log("a user disconnected")
        removeUser(socket.id)
    })
})

ioWeb.on("connection", (socket) => {

    console.log(socket.id)

	socket.emit("me", socket.id)

	socket.on("disconnect", () => {
		socket.broadcast.emit("callEnded")
	})

	socket.on("callUser", (data) => {
		ioWeb.to(data.userToCall).emit("callUser", { signal: data.signalData, from: data.from, name: data.name })
	})

	socket.on("answerCall", (data) => {
		ioWeb.to(data.to).emit("callAccepted", data.signal)
	})
})