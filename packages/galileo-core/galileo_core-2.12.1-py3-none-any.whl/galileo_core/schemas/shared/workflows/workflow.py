from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from galileo_core.schemas.shared.workflows.step import (
    AgentStep,
    AWorkflowStep,
    LlmStep,
    LlmStepAllowedIOType,
    RetrieverStep,
    RetrieverStepAllowedOutputType,
    StepIOType,
    ToolStep,
    WorkflowStep,
    _StepWithChildren,
)


class Workflows(BaseModel):
    workflows: List[AWorkflowStep] = Field(default_factory=list, description="List of workflows.")
    current_workflow: Optional[_StepWithChildren] = Field(default=None, description="Current workflow in the workflow.")

    def add_workflow(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        ground_truth: Optional[str] = None,
    ) -> "Workflows":
        """
        Create a new workflow and add it to the list of workflows.
        Simple usage: `my_workflows.add_workflow("input").add_llm_step("input", "output").conclude_workflow("output")`
        Parameters:
        ----------
            input: str: Input to the node.
            output: Optional[str]: Output of the node.
            name: Optional[str]: Name of the workflow.
            duration_ns: Optional[int]: Duration of the workflow in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the workflow's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this workflow.
            ground_truth: Optional[str]: Ground truth, expected output of the workflow.
        Returns:
        -------
            Workflows: self
        """
        workflow = WorkflowStep(
            input=input,
            output=output or "",
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            ground_truth=ground_truth,
        )
        self.workflows.append(workflow)
        self.current_workflow = workflow
        return self

    def add_agent_workflow(
        self,
        input: str,
        output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        ground_truth: Optional[str] = None,
    ) -> "Workflows":
        """
        Create a new workflow and add it to the list of workflows.
        Simple usage: `my_workflows.add_agent_workflow("input").add_llm_step("input", "output").conclude_workflow("output")`
        Parameters:
        ----------
            input: str: Input to the node.
            output: Optional[str]: Output of the node.
            name: Optional[str]: Name of the workflow.
            duration_ns: Optional[int]: Duration of the workflow in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the workflow's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this workflow.
            ground_truth: Optional[str] = None, Ground truth, expected output of the workflow.
        Returns:
        -------
            Workflows: self
        """
        workflow = AgentStep(
            input=input,
            output=output or "",
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            ground_truth=ground_truth,
        )
        self.workflows.append(workflow)
        self.current_workflow = workflow
        return self

    def add_single_step_workflow(
        self,
        input: LlmStepAllowedIOType,
        output: LlmStepAllowedIOType,
        model: str,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        ground_truth: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> "Workflows":
        """
        Create a new single-step workflow and add it to the list of workflows. This is just if you need a plain llm
        workflow with no surrounding steps.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this step. Feedback from April: Good docs about what model names we use.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            input_tokens: Optional[int]: Number of input tokens.
            output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            ground_truth: Optional[str]: Ground truth, expected output of the workflow.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Workflows: self
        """
        step = LlmStep(
            input=input,
            output=output,
            model=model,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            status_code=status_code,
            ground_truth=ground_truth,
        )
        self.workflows.append(step)
        # Single step workflows are automatically concluded so we reset the current step.
        self.current_workflow = None
        return self

    def _add_step(
        self,
        step: "AWorkflowStep",
    ) -> "Workflows":
        """
        Add a new step to the workflow.

        Parameters:
        ----------
            step: AWorkflowStep: The step to add to the workflow.
        Returns:
        -------
            Workflows: self
        """
        if self.current_workflow is None:
            raise ValueError("A workflow needs to be created in order to add a step.")
        self.current_workflow.steps.append(step)
        # For chain/agent nodes we set current workflow to the created node.
        if isinstance(step, _StepWithChildren):
            self.current_workflow = step
        return self

    def add_llm_step(
        self,
        input: LlmStepAllowedIOType,
        output: LlmStepAllowedIOType,
        model: str,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        status_code: Optional[int] = None,
    ) -> "Workflows":
        """
        Add a new llm step to the current workflow.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this step.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            input_tokens: Optional[int]: Number of input tokens.
            output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Workflows: self
        """
        step = LlmStep(
            input=input,
            output=output,
            model=model,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            temperature=temperature,
            status_code=status_code,
        )
        return self._add_step(step)

    def add_retriever_step(
        self,
        input: StepIOType,
        documents: RetrieverStepAllowedOutputType,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
    ) -> "Workflows":
        """
        Add a new retriever step to the current workflow.

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            documents: Union[List[str], List[Dict[str, str]], List[Document]]: Documents retrieved from the retriever.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Workflows: self
        """
        step = RetrieverStep(
            input=input,
            output=documents,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        return self._add_step(step)

    def add_tool_step(
        self,
        input: StepIOType,
        output: StepIOType,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
    ) -> "Workflows":
        """
        Add a new tool step to the current workflow.

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: StepIOType: Output of the node.
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Workflows: self
        """
        step = ToolStep(
            input=input,
            output=output,
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
            status_code=status_code,
        )
        return self._add_step(step)

    def add_workflow_step(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "Workflows":
        """
        Add a nested workflow step to the workflow. This is useful when you want to create a nested workflow within the
        current workflow. The next step you add will be a child of this workflow. To step out of the nested workflow,
        use conclude_workflow().

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[StepIOType]: Output of the node. This can also be set on conclude_workflow().
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
        Returns:
        -------
            Workflows: self
        """
        step = WorkflowStep(
            parent=self.current_workflow,
            input=input,
            output=output or "",
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
        )
        return self._add_step(step)

    def add_agent_step(
        self,
        input: StepIOType,
        output: Optional[StepIOType] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at_ns: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "Workflows":
        """
        Add a nested agent workflow step to the workflow. This is useful when you want to create a nested workflow
        within the current workflow. The next step you add will be a child of this workflow. To step out of the nested
        workflow, use conclude_workflow().

        Parameters:
        ----------
            input: StepIOType: Input to the node.
            output: Optional[StepIOType]: Output of the node. This can also be set on conclude_workflow().
            name: Optional[str]: Name of the step.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at_ns: Optional[int]: Timestamp of the step's creation.
            metadata: Optional[Dict[str, str]]: Metadata associated with this step.
        Returns:
        -------
            Workflows: self
        """
        step = AgentStep(
            parent=self.current_workflow,
            input=input,
            output=output or "",
            name=name,
            duration_ns=duration_ns,
            created_at_ns=created_at_ns,
            metadata=metadata,
        )
        return self._add_step(step)

    def conclude_workflow(
        self, output: Optional[StepIOType] = None, duration_ns: Optional[int] = None, status_code: Optional[int] = None
    ) -> "Workflows":
        """
        Conclude the workflow by setting the output of the current node. In the case of nested workflows, this will
        point the workflow back to the parent of the current workflow.

        Parameters:
        ----------
            output: Optional[StepIOType]: Output of the node.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Workflows: self
        """
        if self.current_workflow is None:
            raise ValueError("No existing workflow to conclude.")
        self.current_workflow.output = output or ""
        self.current_workflow.status_code = status_code
        if duration_ns is not None:
            self.current_workflow.duration_ns = duration_ns
        # Set the current workflow to the parent of the current workflow.
        self.current_workflow = self.current_workflow.parent
        return self
