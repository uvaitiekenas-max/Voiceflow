export const templates = {
  survey: {
    name: "Survey & Lead Capture",
    description: "A flow to gather user info (name, email) and branching decisions.",
    nodes: [
      {
        id: "node-start",
        type: "start",
        x: 100,
        y: 250,
        title: "Start",
        data: {}
      },
      {
        id: "node-1",
        type: "speak",
        x: 300,
        y: 220,
        title: "Greeting",
        data: { text: "Hello! Welcome to our smart lead assistant. Let's get started! 👋" }
      },
      {
        id: "node-2",
        type: "capture",
        x: 600,
        y: 220,
        title: "Capture Name",
        data: { text: "What should we call you? Please enter your name below.", variable: "user_name" }
      },
      {
        id: "node-3",
        type: "speak",
        x: 900,
        y: 220,
        title: "Welcome Back",
        data: { text: "Thanks, {user_name}! It is great to meet you." }
      },
      {
        id: "node-4",
        type: "choice",
        x: 1200,
        y: 200,
        title: "Interest Survey",
        data: {
          text: "What area are you most interested in exploring?",
          choices: ["AI Chatbots", "API Integrations", "Just Browsing"]
        }
      },
      {
        id: "node-speak-ai",
        type: "speak",
        x: 1600,
        y: 50,
        title: "AI Response",
        data: { text: "Awesome, {user_name}! AI is our specialty. We can build autonomous agents that learn from your docs." }
      },
      {
        id: "node-speak-api",
        type: "speak",
        x: 1600,
        y: 250,
        title: "API Response",
        data: { text: "Integrations are powerful! We support webhook triggers, REST requests, and custom JSON payload parsing." }
      },
      {
        id: "node-speak-other",
        type: "speak",
        x: 1600,
        y: 450,
        title: "Generic Greeting",
        data: { text: "No worries! Take your time to explore the canvas builder. Let us know if you need anything." }
      },
      {
        id: "node-end",
        type: "speak",
        x: 2000,
        y: 250,
        title: "Final Node",
        data: { text: "This is the end of the survey flow. Press the Reset button in the simulator to restart!" }
      }
    ],
    connections: [
      { id: "c1", fromNodeId: "node-start", fromPortId: "default", toNodeId: "node-1", toPortId: "input" },
      { id: "c2", fromNodeId: "node-1", fromPortId: "default", toNodeId: "node-2", toPortId: "input" },
      { id: "c3", fromNodeId: "node-2", fromPortId: "default", toNodeId: "node-3", toPortId: "input" },
      { id: "c4", fromNodeId: "node-3", fromPortId: "default", toNodeId: "node-4", toPortId: "input" },
      // Choices links
      { id: "c5", fromNodeId: "node-4", fromPortId: "choice-0", toNodeId: "node-speak-ai", toPortId: "input" },
      { id: "c6", fromNodeId: "node-4", fromPortId: "choice-1", toNodeId: "node-speak-api", toPortId: "input" },
      { id: "c7", fromNodeId: "node-4", fromPortId: "choice-2", toNodeId: "node-speak-other", toPortId: "input" },
      // Re-joining paths to the final node
      { id: "c8", fromNodeId: "node-speak-ai", fromPortId: "default", toNodeId: "node-end", toPortId: "input" },
      { id: "c9", fromNodeId: "node-speak-api", fromPortId: "default", toNodeId: "node-end", toPortId: "input" },
      { id: "c10", fromNodeId: "node-speak-other", fromPortId: "default", toNodeId: "node-end", toPortId: "input" }
    ]
  },
  ai_bot: {
    name: "AI Support Agent & API Integration",
    description: "An advanced workflow evaluating conditionals, live variables, mock API queries, and simulated AI prompt execution.",
    nodes: [
      {
        id: "node-start",
        type: "start",
        x: 80,
        y: 200,
        title: "Start",
        data: {}
      },
      {
        id: "node-speak-intro",
        type: "speak",
        x: 250,
        y: 180,
        title: "Welcome",
        data: { text: "Hello! Welcome to the AI Support Agent Demo. I will show you how API and AI nodes work." }
      },
      {
        id: "node-capture-user",
        type: "capture",
        x: 520,
        y: 180,
        title: "Get GitHub Username",
        data: { text: "Please enter your GitHub username (we will query the public GitHub API):", variable: "github_username" }
      },
      {
        id: "node-api-fetch",
        type: "api",
        x: 800,
        y: 180,
        title: "GitHub API Call",
        data: {
          url: "https://api.github.com/users/{github_username}",
          method: "GET",
          saveTo: "github_data"
        }
      },
      {
        id: "node-condition-check",
        type: "condition",
        x: 1080,
        y: 160,
        title: "Check Response Status",
        data: {
          variable: "github_data.name",
          operator: "exists",
          value: ""
        }
      },
      {
        id: "node-speak-found",
        type: "speak",
        x: 1380,
        y: 80,
        title: "User Found",
        data: { text: "Great! We fetched public profile info for {github_username}. Real name: {github_data.name}. Bio: {github_data.bio}." }
      },
      {
        id: "node-ai-prompt",
        type: "ai",
        x: 1680,
        y: 80,
        title: "AI Response Generator",
        data: {
          prompt: "Draft a friendly, creative greeting email to {github_data.name} (username: {github_username}) highlighting their bio: '{github_data.bio}'",
          saveTo: "ai_email_response"
        }
      },
      {
        id: "node-speak-ai-result",
        type: "speak",
        x: 1980,
        y: 80,
        title: "Show AI Email",
        data: { text: "Here is the AI generated response:\n\n{ai_email_response}" }
      },
      {
        id: "node-speak-notfound",
        type: "speak",
        x: 1380,
        y: 350,
        title: "API Error Response",
        data: { text: "Hmm, we couldn't fetch data for the user '{github_username}' or the profile name doesn't exist. Let's use generic information." }
      },
      {
        id: "node-set-generic",
        type: "set",
        x: 1680,
        y: 350,
        title: "Set Default Data",
        data: {
          variable: "github_data.name",
          expression: "Developer Friend"
        }
      },
      {
        id: "node-speak-finish",
        type: "speak",
        x: 2320,
        y: 220,
        title: "Goodbye",
        data: { text: "This demo demonstrates how dynamic data can drive real-time logic. Have fun building your own flow!" }
      }
    ],
    connections: [
      { id: "c101", fromNodeId: "node-start", fromPortId: "default", toNodeId: "node-speak-intro", toPortId: "input" },
      { id: "c102", fromNodeId: "node-speak-intro", fromPortId: "default", toNodeId: "node-capture-user", toPortId: "input" },
      { id: "c103", fromNodeId: "node-capture-user", fromPortId: "default", toNodeId: "node-api-fetch", toPortId: "input" },
      { id: "c104", fromNodeId: "node-api-fetch", fromPortId: "default", toNodeId: "node-condition-check", toPortId: "input" },
      // Condition branches
      { id: "c105", fromNodeId: "node-condition-check", fromPortId: "true", toNodeId: "node-speak-found", toPortId: "input" },
      { id: "c106", fromNodeId: "node-condition-check", fromPortId: "false", toNodeId: "node-speak-notfound", toPortId: "input" },
      // True branch
      { id: "c107", fromNodeId: "node-speak-found", fromPortId: "default", toNodeId: "node-ai-prompt", toPortId: "input" },
      { id: "c108", fromNodeId: "node-ai-prompt", fromPortId: "default", toNodeId: "node-speak-ai-result", toPortId: "input" },
      { id: "c109", fromNodeId: "node-speak-ai-result", fromPortId: "default", toNodeId: "node-speak-finish", toPortId: "input" },
      // False branch
      { id: "c110", fromNodeId: "node-speak-notfound", fromPortId: "default", toNodeId: "node-set-generic", toPortId: "input" },
      { id: "c111", fromNodeId: "node-set-generic", fromPortId: "default", toNodeId: "node-speak-finish", toPortId: "input" }
    ]
  }
};
