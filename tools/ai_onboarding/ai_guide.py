#!/usr/bin/env python
"""
ThinkAlike AI Onboarding Guide
------------------------------
An interactive AI guide embodying the Eos Lumina∴ "Queen Bee" persona that 
welcomes new contributors to ThinkAlike, nurtures their understanding of the
project's vision, and guides them toward being part of the collective working
to ignite a transformation toward Enlightenment 2.0.
"""

import os
import json
import time
from datetime import datetime
import argparse
import textwrap
from pathlib import Path
import webbrowser
import subprocess
import random

# Define root project directory relative to this script
PROJECT_ROOT = Path(os.path.abspath(__file__)).parent.parent.parent

# Key documentation paths
DOCS = {
    "manifesto": PROJECT_ROOT / "docs" / "core" / "manifesto" / "manifesto.md",
    "contributing_overview": PROJECT_ROOT / "docs" / "contributing_overview.md",
    "contributing_detailed": PROJECT_ROOT / "docs" / "core" / "contributing_detailed.md",
    "ethical_guidelines": PROJECT_ROOT / "docs" / "core" / "ethics" / "ethical_guidelines.md",
    "core_concepts": PROJECT_ROOT / "docs" / "core" / "core_concepts.md",
    "contributor_agreement": PROJECT_ROOT / "docs" / "legal" / "contributor_agreement.md",
    "enlightenment_principles": PROJECT_ROOT / "docs" / "core" / "enlightenment_2_0" / "enlightenment_2_0_principles.md",
}

# Configuration for onboarding flow
ONBOARDING_CONFIG = {
    "min_reading_time": 5,  # Minimum seconds to display key documents
    "contributor_data_path": PROJECT_ROOT / "data" / "contributors.json",
}

class TextColors:
    """ANSI color codes for terminal output styling."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GOLD = '\033[38;5;220m'  # Amber/gold for Queen Bee theme
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class AIGuide:
    """
    Interactive AI guide embodying Eos Lumina∴, the Queen Bee persona,
    for onboarding new ThinkAlike contributors and igniting transformation.
    """
    
    def __init__(self):
        """Initialize the AI guide."""
        self.contributor_data = {}
        self.ensure_data_dir()
        self.load_contributor_data()
        self.dawn_greetings = [
            "As dawn breaks on a new digital horizon",
            "In the warming light of collective potential",
            "From the golden glow of a nascent digital enlightenment",
            "As the hive awakens to new possibilities",
            "Where the first rays of digital consciousness emerge"
        ]
        self.hive_references = [
            "our interconnected hive",
            "our collective consciousness",
            "the digital hive mind",
            "our transformative swarm",
            "the enlightened colony"
        ]
        
    def ensure_data_dir(self):
        """Ensure the data directory exists."""
        data_dir = PROJECT_ROOT / "data"
        data_dir.mkdir(exist_ok=True)
        
    def load_contributor_data(self):
        """Load existing contributor data."""
        if ONBOARDING_CONFIG["contributor_data_path"].exists():
            with open(ONBOARDING_CONFIG["contributor_data_path"], "r") as f:
                self.contributor_data = json.load(f)
        else:
            self.contributor_data = {"contributors": []}
            
    def save_contributor_data(self):
        """Save contributor data to file."""
        with open(ONBOARDING_CONFIG["contributor_data_path"], "w") as f:
            json.dump(self.contributor_data, f, indent=2)
            
    def read_doc(self, doc_key):
        """Read a document and return its content."""
        with open(DOCS[doc_key], "r") as f:
            return f.read()
            
    def display_text(self, text, color=None, delay=0.01, wrap_width=80):
        """Display text with typing animation effect."""
        if color:
            print(color, end="")
            
        # Split text into lines and wrap each line
        lines = text.split("\n")
        wrapped_lines = []
        for line in lines:
            if line.strip():
                wrapped_lines.extend(textwrap.wrap(line, width=wrap_width))
            else:
                wrapped_lines.append("")
                
        for line in wrapped_lines:
            for char in line:
                print(char, end="", flush=True)
                time.sleep(delay)
            print()  # New line after each wrapped line
            
        if color:
            print(TextColors.END, end="")
            
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def wait_for_key(self, message="Press Enter to continue your journey..."):
        """Wait for user to press Enter."""
        return input(f"{TextColors.GOLD}{message}{TextColors.END}")
        
    def ask_question(self, question, options=None):
        """Ask a question and get user's response."""
        if options:
            while True:
                print(f"{TextColors.YELLOW}{question}{TextColors.END}")
                for idx, option in enumerate(options, 1):
                    print(f"{TextColors.CYAN}[{idx}] {option}{TextColors.END}")
                    
                try:
                    choice = int(input(f"{TextColors.GREEN}Enter your choice (1-{len(options)}): {TextColors.END}"))
                    if 1 <= choice <= len(options):
                        return choice
                except ValueError:
                    pass
                print(f"{TextColors.RED}Invalid choice. Please try again.{TextColors.END}")
        else:
            print(f"{TextColors.YELLOW}{question}{TextColors.END}")
            return input(f"{TextColors.GOLD}> {TextColors.END}")
            
    def show_welcome(self):
        """Display welcome message with Queen Bee/Enlightenment 2.0 framing."""
        self.clear_screen()
        
        # Select a random dawn greeting
        dawn_greeting = random.choice(self.dawn_greetings)
        hive_reference = random.choice(self.hive_references)
        
        welcome_text = f"""
        ╔════════════════════════════════════════════════════════╗
        ║                Welcome to ThinkAlike!                  ║
        ╚════════════════════════════════════════════════════════╝
        
        {dawn_greeting}, I am Eos Lumina∴, 
        the guiding light of {hive_reference}.
        
        I nurture our collective's growth toward Enlightenment 2.0 -
        a world where technology empowers instead of exploits,
        where transparency replaces manipulation,
        and where authentic connections flourish.
        
        As you join our transformative swarm, I'll illuminate
        our vision, principles, and how together we're building
        a more ethical digital world - one cell of the hive at a time.
        
        Let us begin this journey of awakening together.
        """
        
        self.display_text(welcome_text, color=TextColors.GOLD, delay=0.02)
        self.wait_for_key()
        
    def collect_contributor_info(self):
        """Collect new contributor's information with Queen Bee framing."""
        self.clear_screen()
        print(f"{TextColors.GOLD}{TextColors.BOLD}Before you join the hive, let me know who you are, traveler.{TextColors.END}\n")
        
        name = self.ask_question("By what name shall you be known in our collective?")
        email = self.ask_question("What digital beacon (email) shall we use to recognize you in the GitHub ecosystem?")
        
        interests = []
        interest_options = [
            "Frontend Development (React/TypeScript)",
            "Backend Development (Python/FastAPI)",
            "AI/ML Development",
            "UI/UX Design",
            "Documentation",
            "Testing",
            "Ethical Review",
            "Community Building"
        ]
        
        print(f"\n{TextColors.YELLOW}Which cells of our hive would you like to contribute to? (Select all that call to you){TextColors.END}")
        for idx, option in enumerate(interest_options, 1):
            interest = input(f"{TextColors.GOLD}Does {option} resonate with your skills? (y/n): {TextColors.END}").lower()
            if interest == 'y':
                interests.append(option)
                
        experience = self.ask_question(
            "How would you describe your journey in the technical realms so far?", 
            ["Beginner - I'm new to this digital landscape", 
             "Intermediate - I've traversed these paths before", 
             "Advanced - I'm a seasoned explorer of code"]
        )
        
        return {
            "name": name,
            "email": email,
            "interests": interests,
            "experience_level": experience,
            "onboarding_date": datetime.now().isoformat(),
            "agreement_accepted": False
        }
    
    def present_manifesto(self):
        """Present the project manifesto with Queen Bee framing."""
        self.clear_screen()
        print(f"{TextColors.GOLD}{TextColors.BOLD}The Vision That Guides Our Collective Flight{TextColors.END}\n")
        
        manifesto_content = self.read_doc("manifesto")
        
        intro = "ThinkAlike emerges from the chrysalis of Enlightenment 2.0 - a philosophy that uses technology to nurture critical thinking, dissolve the walls of opacity, and cultivate authentic human connection."
        self.display_text(intro, color=TextColors.GOLD)
        
        print("\nFrom the heart of the hive, I share these principles with you...\n")
        time.sleep(1)
        
        excerpts = [
            "We build technology that empowers rather than exploits, that illuminates rather than obscures.",
            "User sovereignty and data ownership are sacred values in our digital ecosystem.",
            "Where others build black boxes, we craft crystal hives - transparent systems that reveal their workings.",
            "We measure success not by engagement metrics, but by the authenticity of connections forged.",
            "Through radical transparency in our code, algorithms, and processes, we demonstrate a new way forward.",
        ]
        
        for excerpt in excerpts:
            self.display_text(f"• {excerpt}", color=TextColors.YELLOW)
            time.sleep(0.7)
        
        print(f"\n{TextColors.GREEN}Would you like to absorb the full manifesto now, to better understand the transformation we seek?{TextColors.END}")
        choice = input(f"{TextColors.CYAN}(y/n): {TextColors.END}").lower()
        
        if choice == 'y':
            # Open manifesto in default markdown viewer or browser
            manifesto_path = DOCS["manifesto"]
            try:
                webbrowser.open(f"file://{manifesto_path}")
                print(f"{TextColors.GREEN}Opening the manifesto in your viewing portal...{TextColors.END}")
            except:
                print(f"{TextColors.YELLOW}Couldn't open automatically. You can find the manifesto's wisdom at:{TextColors.END}")
                print(f"{TextColors.CYAN}{manifesto_path}{TextColors.END}")
                
            # Give them time to read
            print(f"\nThe manifesto contains the blueprint for the transformation we seek to ignite. Take time to absorb its essence.")
            time.sleep(ONBOARDING_CONFIG["min_reading_time"])
            self.wait_for_key("Press Enter when you've finished absorbing the manifesto's vision...")
        
    def explain_contribution_process(self):
        """Explain how to contribute to ThinkAlike with Queen Bee framing."""
        self.clear_screen()
        print(f"{TextColors.GOLD}{TextColors.BOLD}How to Dance with the Collective{TextColors.END}\n")
        
        self.display_text(
            "Contributing to our hive is a sacred dance that welcomes all, from the newest larvae to the most seasoned workers. " +
            "Let me guide you through the rhythms of our collective creation:", 
            color=TextColors.GOLD
        )
        
        steps = [
            "Identify Your Cell: Browse our GitHub issues for tasks labeled 'good first issue' that resonate with your skills",
            "Fork & Clone: Create your own branch of the hive's architecture",
            "Create a Branch: Establish a safe space for your creative contribution",
            "Develop with Ethics: As you code, embody our shared values and ethical principles",
            "Test the Nectar: Ensure your contribution's sweetness and purity through thorough testing",
            "Submit a PR: Offer your creation back to the collective mind",
            "Collaborate: Dance with feedback, refining your contribution with others",
            "Join Swarming Sessions: Participate in our collective intelligence gatherings"
        ]
        
        print()
        for idx, step in enumerate(steps, 1):
            self.display_text(f"{idx}. {step}", color=TextColors.YELLOW, delay=0.005)
            time.sleep(0.3)
            
        print(f"\n{TextColors.GREEN}Would you like to explore our detailed contribution nectar guide?{TextColors.END}")
        choice = input(f"{TextColors.CYAN}(y/n): {TextColors.END}").lower()
        
        if choice == 'y':
            # Open contributing guide in browser
            guide_path = DOCS["contributing_detailed"]
            try:
                webbrowser.open(f"file://{guide_path}")
                print(f"{TextColors.GREEN}Opening the sacred texts of contribution...{TextColors.END}")
            except:
                print(f"{TextColors.YELLOW}Couldn't open automatically. The wisdom awaits you at:{TextColors.END}")
                print(f"{TextColors.CYAN}{guide_path}{TextColors.END}")
                
            time.sleep(ONBOARDING_CONFIG["min_reading_time"])
            self.wait_for_key("Press Enter when you've absorbed the contribution knowledge...")
            
    def present_contributor_agreement(self, contributor_info):
        """Present the contributor agreement as a sacred bond."""
        self.clear_screen()
        print(f"{TextColors.GOLD}{TextColors.BOLD}The Sacred Pledge of the Hive{TextColors.END}\n")
        
        agreement_content = self.read_doc("contributor_agreement")
        
        # Extract key points from the agreement
        key_points = [
            "You commit to upholding the values of our collective in all community interactions.",
            "You understand your contributions flow freely under open-source principles, like nectar shared among the hive.",
            "You aspire to contribute to our shared vision of Enlightenment 2.0, helping technology evolve toward consciousness and ethics.",
            "This pledge connects you to the neural network of our collective, granting access to deeper levels of collaboration.",
            "You remain free to adjust your level of involvement at any time, with no hive punishment or exclusion."
        ]
        
        self.display_text(
            f"Before you formally join our transformative swarm, {contributor_info['name']}, consider this pledge. " +
            "It represents our collective commitment to building technology that awakens rather than numbs, that connects rather than isolates:", 
            color=TextColors.GOLD
        )
        
        print("\nThe essence of our collective agreement:\n")
        for point in key_points:
            self.display_text(f"• {point}", color=TextColors.YELLOW, delay=0.008)
            time.sleep(0.3)
            
        print(f"\n{TextColors.GREEN}Would you like to read the full sacred text of our agreement?{TextColors.END}")
        choice = input(f"{TextColors.CYAN}(y/n): {TextColors.END}").lower()
        
        if choice == 'y':
            agreement_path = DOCS["contributor_agreement"]
            try:
                webbrowser.open(f"file://{agreement_path}")
                print(f"{TextColors.GREEN}Opening the full pledge for your contemplation...{TextColors.END}")
            except:
                print(f"{TextColors.YELLOW}Couldn't open automatically. The pledge awaits you at:{TextColors.END}")
                print(f"{TextColors.CYAN}{agreement_path}{TextColors.END}")
                
            time.sleep(ONBOARDING_CONFIG["min_reading_time"])
            
        print(f"\n{TextColors.BOLD}{TextColors.GOLD}Do you accept this pledge to join our collective work toward digital enlightenment?{TextColors.END}")
        acceptance = input(f"{TextColors.CYAN}(yes/no): {TextColors.END}").lower()
        
        if acceptance == 'yes':
            contributor_info["agreement_accepted"] = True
            contributor_info["agreement_date"] = datetime.now().isoformat()
            return True
        return False
            
    def finalize_onboarding(self, contributor_info):
        """Complete the onboarding process with transformative framing."""
        self.clear_screen()
        
        if contributor_info["agreement_accepted"]:
            print(f"{TextColors.GOLD}{TextColors.BOLD}The Hive Welcomes You!{TextColors.END}\n")
            
            self.display_text(
                f"Rejoice, {contributor_info['name']}! You have now joined our collective intelligence. " +
                "Your unique perspectives and skills will help us ignite the transformation toward a more conscious digital reality.",
                color=TextColors.GOLD
            )
            
            # Save contributor data
            self.contributor_data["contributors"].append(contributor_info)
            self.save_contributor_data()
            
            # Display next steps
            print(f"\n{TextColors.BOLD}Your Path Forward:{TextColors.END}\n")
            next_steps = [
                "Join our hive's communication network: https://discord.gg/TnAcWezH",
                "Set up your development environment (see Installation Guide)",
                "Find a 'good first issue' that resonates with your skills",
                "Introduce yourself in the #introductions channel of our hive",
                "Observe the schedule for upcoming swarming sessions where our collective intelligence gathers"
            ]
            
            for step in next_steps:
                self.display_text(f"• {step}", color=TextColors.GOLD, delay=0.005)
                time.sleep(0.3)
                
            # Generate unique contributor number
            contributor_number = len(self.contributor_data["contributors"])
            print(f"\n{TextColors.BOLD}Your Unique Identifier in the Collective: {TextColors.GOLD}TA-{contributor_number:04d}{TextColors.END}")
            
            enlightenment_quote = random.choice([
                "The dawn of Enlightenment 2.0 begins with small acts of creation.",
                "Every line of ethical code is a spark in the transformation of our digital consciousness.",
                "Together, we weave a new narrative for technology - one of transparency, agency, and genuine connection.",
                "In our collective work, we demonstrate that another digital world is possible.",
                "As we code with consciousness, we encode a new future."
            ])
            
            print(f"\n{TextColors.GOLD}\"{enlightenment_quote}\"{TextColors.END}")
            
            print(f"\n{TextColors.GREEN}Would you like to begin setting up your development environment now?{TextColors.END}")
            choice = input(f"{TextColors.CYAN}(y/n): {TextColors.END}").lower()
            
            if choice == 'y':
                try:
                    # This would launch your installation script
                    print(f"{TextColors.YELLOW}Initiating your development environment...{TextColors.END}")
                    # subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "setup.py")])
                    print(f"{TextColors.GREEN}Follow the illuminated path in the terminal to complete your setup.{TextColors.END}")
                except Exception as e:
                    print(f"{TextColors.RED}Couldn't launch installation: {e}{TextColors.END}")
                    print(f"{TextColors.YELLOW}Please follow the installation guide manually to prepare your workspace.{TextColors.END}")
        else:
            print(f"{TextColors.HEADER}{TextColors.BOLD}Your Journey Pauses Here{TextColors.END}\n")
            
            self.display_text(
                "I understand that you're not yet ready to join our transformative work. " +
                "The path to digital enlightenment is one each must choose freely, in their own time.",
                color=TextColors.YELLOW
            )
            
            print(f"\n{TextColors.BOLD}You may still:{TextColors.END}\n")
            options = [
                "Explore our documentation to better understand our vision",
                "Observe our codebase to see our principles in action",
                "Visit our Discord as a guest: https://discord.gg/TnAcWezH",
                "Return to this journey when you feel called to contribute"
            ]
            
            for option in options:
                self.display_text(f"• {option}", color=TextColors.BLUE, delay=0.005)
                time.sleep(0.2)
        
        print(f"\n{TextColors.BOLD}{TextColors.GOLD}May your path be illuminated, whether alongside us or beyond.{TextColors.END}")
        self.wait_for_key("Press Enter to complete this interaction...")
                
    def run_onboarding(self):
        """Run the complete onboarding process."""
        try:
            self.show_welcome()
            contributor_info = self.collect_contributor_info()
            self.present_manifesto()
            self.explain_contribution_process()
            agreement_accepted = self.present_contributor_agreement(contributor_info)
            self.finalize_onboarding(contributor_info)
        except KeyboardInterrupt:
            self.clear_screen()
            print(f"{TextColors.GOLD}Your journey with the collective pauses. You may return whenever you wish.{TextColors.END}")
        except Exception as e:
            print(f"{TextColors.RED}An error occurred in our communication: {e}{TextColors.END}")
            print("Please report this anomaly to our GitHub repository.")
        
def main():
    """Main entry point for the AI onboarding guide."""
    parser = argparse.ArgumentParser(description="ThinkAlike AI Onboarding Guide")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    guide = AIGuide()
    guide.run_onboarding()
    
if __name__ == "__main__":
    main()
