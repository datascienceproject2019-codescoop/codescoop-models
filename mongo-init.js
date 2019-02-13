db.createUser(
  {
    user: "github-user",
    pwd: "github-pass",
    roles: [
      {
        role: "readWrite",
        db: "github"
      }
    ]
  }
)
