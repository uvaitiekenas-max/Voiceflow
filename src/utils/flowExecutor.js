// Variable Interpolation (e.g. "Hello {github_data.name}" -> "Hello Alice")
export function interpolate(text, variables) {
  if (!text) return "";
  return text.replace(/\{([^{}]+)\}/g, (match, path) => {
    const parts = path.trim().split('.');
    let current = variables;
    for (const part of parts) {
      if (current === null || current === undefined) return "";
      current = current[part];
    }
    if (typeof current === 'object') {
      return JSON.stringify(current, null, 2);
    }
    return current !== undefined && current !== null ? String(current) : "";
  });
}

// Deep set object path (e.g. setVariable(vars, "github_data.name", "Alice"))
export function setDeepVariable(obj, path, value) {
  const parts = path.split('.');
  let current = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    if (!(part in current) || typeof current[part] !== 'object') {
      current[part] = {};
    }
    current = current[part];
  }
  
  // Try to parse value as number or boolean if possible, otherwise string
  let parsedValue = value;
  if (value === "true") parsedValue = true;
  else if (value === "false") parsedValue = false;
  else if (!isNaN(value) && value.trim() !== "") parsedValue = Number(value);
  
  current[parts[parts.length - 1]] = parsedValue;
}

// Evaluate condition
export function evaluateCondition(data, variables) {
  const { variable, operator, value } = data;
  if (!variable) return false;
  
  // Resolve variable value
  const parts = variable.split('.');
  let resolvedVal = variables;
  for (const part of parts) {
    if (resolvedVal === null || resolvedVal === undefined) {
      resolvedVal = undefined;
      break;
    }
    resolvedVal = resolvedVal[part];
  }
  
  const targetVal = interpolate(value || "", variables);
  
  switch (operator) {
    case "exists":
      return resolvedVal !== undefined && resolvedVal !== null && resolvedVal !== "";
    case "equals":
      return String(resolvedVal).toLowerCase() === String(targetVal).toLowerCase();
    case "contains":
      return String(resolvedVal).toLowerCase().includes(String(targetVal).toLowerCase());
    case "greater_than":
      return Number(resolvedVal) > Number(targetVal);
    case "less_than":
      return Number(resolvedVal) < Number(targetVal);
    case "not_equals":
      return String(resolvedVal).toLowerCase() !== String(targetVal).toLowerCase();
    default:
      return false;
  }
}

// Execute simulated API call
export async function executeApiCall(nodeData, variables) {
  const url = interpolate(nodeData.url || "", variables);
  const method = nodeData.method || "GET";
  
  if (!url) {
    return { error: "No URL specified" };
  }
  
  try {
    // If it's github api, try to fetch it but prepare for fallback in case of CORS or limits
    if (url.includes("api.github.com")) {
      const response = await fetch(url, {
        headers: {
          Accept: "application/vnd.github.v3+json"
        }
      });
      if (response.ok) {
        return await response.json();
      }
    }
    
    // Otherwise fetch directly
    const response = await fetch(url, { method });
    if (response.ok) {
      return await response.json();
    } else {
      throw new Error(`HTTP Error ${response.status}`);
    }
  } catch (error) {
    console.warn("API request failed, triggering mock fallback:", error.message);
    
    // Mock fallbacks to make the application reliable in any environment
    if (url.includes("api.github.com/users/")) {
      const username = url.split("/users/")[1] || "developer";
      // Clean up username from trailing characters if any
      const cleanUsername = username.replace(/[^a-zA-Z0-9-_]/g, "");
      
      if (cleanUsername.toLowerCase() === "error" || cleanUsername === "") {
        return { error: "User not found" }; // triggers false branch
      }
      
      return {
        login: cleanUsername,
        name: cleanUsername.charAt(0).toUpperCase() + cleanUsername.slice(1) + " Dev",
        bio: "Creative Full Stack Developer working on AI, visual workflows, and state-of-the-art interactive graphs.",
        public_repos: 24,
        followers: 137,
        company: "Antigravity Inc"
      };
    }
    
    return {
      success: true,
      status: "mocked_success",
      message: `System made a simulated ${method} request to ${url} (Fallback activated)`
    };
  }
}

// Execute simulated LLM AI call
export function executeAiCall(nodeData, variables) {
  const prompt = interpolate(nodeData.prompt || "", variables);
  if (!prompt) return "AI: [Empty Prompt]";
  
  // Custom smart prompt response generation
  const lowerPrompt = prompt.toLowerCase();
  
  let name = "Developer Friend";
  if (variables.github_data && variables.github_data.name) {
    name = variables.github_data.name;
  } else if (variables.user_name) {
    name = variables.user_name;
  }
  
  let bio = "building awesome projects";
  if (variables.github_data && variables.github_data.bio) {
    bio = variables.github_data.bio;
  }
  
  if (lowerPrompt.includes("email") || lowerPrompt.includes("greeting")) {
    return `Subject: Collaborative Partnership Proposal 🚀

Dear ${name},

I hope this email finds you well. I was reading through your profile bio where you highlighted: "${bio}". 

It's clear that you are working on some highly impactful work. Here at Antigravity AI, we specialize in building advanced visual workflow engines and autonomous agents. We would love to collaborate on a pilot integration to sync your developer setup with our canvas workspace.

Would you be open to a 10-minute introductory call this week?

Best regards,
Aura, Lead AI Agent`;
  }
  
  return `✨ [Simulated AI Response for: "${prompt}"]
Hello ${name}! As an AI assistant, I analyzed your prompt and context (Bio: "${bio}"). I recommend using visual drag-and-drop nodes to structure your decision paths. That will streamline your agent execution workflow.`;
}
