# MarkCheck

MarkCheck is a platform for creating and managing Kanban boards using Markdown files. It allows users to define tasks and organize them into columns directly within Markdown, providing a simple and lightweight solution for task management.

## Features

- **Markdown-Based Kanban Boards**: Define tasks and columns in Markdown files.
- **User Authentication**: Sign in with Google to save and manage your boards.
- **MongoDB Integration**: Store user data and board configurations securely.
- **Responsive Design**: Access your boards on any device with a clean and intuitive interface.

## Project Structure

```
markcheck
├── config.py
├── main.py
├── requirements.txt
├── vercel.json
├── .env
├── .gitignore
├── README.md
├── static
│   ├── styles.css
├── templates
│   ├── dashboard.html
│   ├── login.html
│   └── index.html
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/markcheck.git
   cd markcheck
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   - Set up a MongoDB database.
   - Create a `.env` file with the following variables:
     ```
     SECRET_KEY=your_secret_key
     MONGO_URI=your_mongo_uri
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     ```

## Running the Application

Start the application with:
```bash
python main.py
```

Access the app at [http://localhost:5000](http://localhost:5000).

## Usage

1. **Login**: Sign in with your Google account to access your boards.
2. **Create Boards**: Use Markdown syntax to define tasks and columns.
3. **Manage Tasks**: Drag and drop tasks between columns to update their status.

## Example Markdown Syntax

```markdown
# To Do
- [ ] Task 1
- [ ] Task 2

# In Progress
- [ ] Task 3

# Done
- [x] Task 4
```

## Deployment

MarkCheck is configured for deployment on Vercel. Use the provided `vercel.json` file for seamless deployment.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for new features or improvements.

## License

This project is licensed under the MIT License.
