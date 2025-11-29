import type * as z from "zod";
import * as v0_1 from "./0.1.js";
import * as v0_2 from "./0.2.js";
import * as v0_3 from "./0.3.js";
type McpbManifestV0_1 = z.infer<typeof v0_1.McpbManifestSchema>;
type McpbManifestV0_2 = z.infer<typeof v0_2.McpbManifestSchema>;
type McpbManifestV0_3 = z.infer<typeof v0_3.McpbManifestSchema>;
/**
 * Union type representing any supported manifest version.
 * This is the return type of validateManifest.
 */
type ValidatedManifest = McpbManifestV0_1 | McpbManifestV0_2 | McpbManifestV0_3;
/**
 * Validates a manifest using the appropriate schema based on its manifest_version.
 *
 * This function automatically detects the manifest version from the data and applies
 * the correct schema. This avoids TypeScript "excessively deep" errors that can occur
 * when using union schemas across package boundaries.
 *
 * @param data - The manifest data to validate
 * @returns The validated manifest with the correct type
 * @throws ZodError if validation fails
 *
 * @example
 * ```typescript
 * import { validateManifest } from '@anthropic-ai/mcpb/browser';
 *
 * const manifest = validateManifest(unknownData);
 * // manifest is typed as McpbManifestAny (union of all versions)
 * ```
 */
export declare function validateManifest(data: unknown): ValidatedManifest;
/**
 * Validates a manifest using the appropriate schema, returning a Result-style object.
 *
 * @param data - The manifest data to validate
 * @returns An object with either { success: true, data } or { success: false, error }
 *
 * @example
 * ```typescript
 * import { validateManifestSafe } from '@anthropic-ai/mcpb/browser';
 *
 * const result = validateManifestSafe(unknownData);
 * if (result.success) {
 *   console.log(result.data);
 * } else {
 *   console.error(result.error);
 * }
 * ```
 */
export declare function validateManifestSafe(data: unknown): {
    success: true;
    data: ValidatedManifest;
} | {
    success: false;
    error: unknown;
};
/**
 * Get the appropriate schema for a given manifest version.
 * Useful when you need to work with the schema directly.
 *
 * @param version - The manifest version (e.g., "0.1", "0.2", "0.3")
 * @returns The schema for that version
 *
 * @example
 * ```typescript
 * import { getSchemaForVersion } from '@anthropic-ai/mcpb/browser';
 *
 * const schema = getSchemaForVersion("0.2");
 * const result = schema.safeParse(data);
 * ```
 */
export declare function getSchemaForVersion(version: "0.1" | "0.2" | "0.3"): z.ZodEffects<z.ZodObject<{
    $schema: z.ZodOptional<z.ZodString>;
    dxt_version: z.ZodOptional<z.ZodLiteral<"0.1">>;
    manifest_version: z.ZodOptional<z.ZodLiteral<"0.1">>;
    name: z.ZodString;
    display_name: z.ZodOptional<z.ZodString>;
    version: z.ZodString;
    description: z.ZodString;
    long_description: z.ZodOptional<z.ZodString>;
    author: z.ZodObject<{
        name: z.ZodString;
        email: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    }, {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    }>;
    repository: z.ZodOptional<z.ZodObject<{
        type: z.ZodString;
        url: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        url: string;
        type: string;
    }, {
        url: string;
        type: string;
    }>>;
    homepage: z.ZodOptional<z.ZodString>;
    documentation: z.ZodOptional<z.ZodString>;
    support: z.ZodOptional<z.ZodString>;
    icon: z.ZodOptional<z.ZodString>;
    screenshots: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    server: z.ZodObject<{
        type: z.ZodEnum<["python", "node", "binary"]>;
        entry_point: z.ZodString;
        mcp_config: z.ZodObject<{
            command: z.ZodString;
            args: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
            env: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>;
        } & {
            platform_overrides: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodObject<{
                command: z.ZodOptional<z.ZodString>;
                args: z.ZodOptional<z.ZodOptional<z.ZodArray<z.ZodString, "many">>>;
                env: z.ZodOptional<z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>>;
            }, "strict", z.ZodTypeAny, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }>>>;
        }, "strict", z.ZodTypeAny, {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        }, {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        }>;
    }, "strict", z.ZodTypeAny, {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    }, {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    }>;
    tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        name: string;
        description?: string | undefined;
    }, {
        name: string;
        description?: string | undefined;
    }>, "many">>;
    tools_generated: z.ZodOptional<z.ZodBoolean>;
    prompts: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
        arguments: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
        text: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }, {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }>, "many">>;
    prompts_generated: z.ZodOptional<z.ZodBoolean>;
    keywords: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    license: z.ZodOptional<z.ZodString>;
    compatibility: z.ZodOptional<z.ZodObject<{
        claude_desktop: z.ZodOptional<z.ZodString>;
        platforms: z.ZodOptional<z.ZodArray<z.ZodEnum<["darwin", "win32", "linux"]>, "many">>;
        runtimes: z.ZodOptional<z.ZodObject<{
            python: z.ZodOptional<z.ZodString>;
            node: z.ZodOptional<z.ZodString>;
        }, "strict", z.ZodTypeAny, {
            python?: string | undefined;
            node?: string | undefined;
        }, {
            python?: string | undefined;
            node?: string | undefined;
        }>>;
    }, "strict", z.ZodTypeAny, {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    }, {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    }>>;
    user_config: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodObject<{
        type: z.ZodEnum<["string", "number", "boolean", "directory", "file"]>;
        title: z.ZodString;
        description: z.ZodString;
        required: z.ZodOptional<z.ZodBoolean>;
        default: z.ZodOptional<z.ZodUnion<[z.ZodString, z.ZodNumber, z.ZodBoolean, z.ZodArray<z.ZodString, "many">]>>;
        multiple: z.ZodOptional<z.ZodBoolean>;
        sensitive: z.ZodOptional<z.ZodBoolean>;
        min: z.ZodOptional<z.ZodNumber>;
        max: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }>>>;
    _meta: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodRecord<z.ZodString, z.ZodAny>>>;
}, "strict", z.ZodTypeAny, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.1" | undefined;
    manifest_version?: "0.1" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
}, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.1" | undefined;
    manifest_version?: "0.1" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
}>, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.1" | undefined;
    manifest_version?: "0.1" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
}, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.1" | undefined;
    manifest_version?: "0.1" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
}> | z.ZodEffects<z.ZodObject<{
    $schema: z.ZodOptional<z.ZodString>;
    dxt_version: z.ZodOptional<z.ZodLiteral<"0.2">>;
    manifest_version: z.ZodOptional<z.ZodLiteral<"0.2">>;
    name: z.ZodString;
    display_name: z.ZodOptional<z.ZodString>;
    version: z.ZodString;
    description: z.ZodString;
    long_description: z.ZodOptional<z.ZodString>;
    author: z.ZodObject<{
        name: z.ZodString;
        email: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    }, {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    }>;
    repository: z.ZodOptional<z.ZodObject<{
        type: z.ZodString;
        url: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        url: string;
        type: string;
    }, {
        url: string;
        type: string;
    }>>;
    homepage: z.ZodOptional<z.ZodString>;
    documentation: z.ZodOptional<z.ZodString>;
    support: z.ZodOptional<z.ZodString>;
    icon: z.ZodOptional<z.ZodString>;
    screenshots: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    server: z.ZodObject<{
        type: z.ZodEnum<["python", "node", "binary"]>;
        entry_point: z.ZodString;
        mcp_config: z.ZodObject<{
            command: z.ZodString;
            args: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
            env: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>;
        } & {
            platform_overrides: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodObject<{
                command: z.ZodOptional<z.ZodString>;
                args: z.ZodOptional<z.ZodOptional<z.ZodArray<z.ZodString, "many">>>;
                env: z.ZodOptional<z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>>;
            }, "strict", z.ZodTypeAny, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }>>>;
        }, "strict", z.ZodTypeAny, {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        }, {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        }>;
    }, "strict", z.ZodTypeAny, {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    }, {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    }>;
    tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        name: string;
        description?: string | undefined;
    }, {
        name: string;
        description?: string | undefined;
    }>, "many">>;
    tools_generated: z.ZodOptional<z.ZodBoolean>;
    prompts: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
        arguments: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
        text: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }, {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }>, "many">>;
    prompts_generated: z.ZodOptional<z.ZodBoolean>;
    keywords: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    license: z.ZodOptional<z.ZodString>;
    privacy_policies: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    compatibility: z.ZodOptional<z.ZodObject<{
        claude_desktop: z.ZodOptional<z.ZodString>;
        platforms: z.ZodOptional<z.ZodArray<z.ZodEnum<["darwin", "win32", "linux"]>, "many">>;
        runtimes: z.ZodOptional<z.ZodObject<{
            python: z.ZodOptional<z.ZodString>;
            node: z.ZodOptional<z.ZodString>;
        }, "strict", z.ZodTypeAny, {
            python?: string | undefined;
            node?: string | undefined;
        }, {
            python?: string | undefined;
            node?: string | undefined;
        }>>;
    }, "strict", z.ZodTypeAny, {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    }, {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    }>>;
    user_config: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodObject<{
        type: z.ZodEnum<["string", "number", "boolean", "directory", "file"]>;
        title: z.ZodString;
        description: z.ZodString;
        required: z.ZodOptional<z.ZodBoolean>;
        default: z.ZodOptional<z.ZodUnion<[z.ZodString, z.ZodNumber, z.ZodBoolean, z.ZodArray<z.ZodString, "many">]>>;
        multiple: z.ZodOptional<z.ZodBoolean>;
        sensitive: z.ZodOptional<z.ZodBoolean>;
        min: z.ZodOptional<z.ZodNumber>;
        max: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }>>>;
}, "strict", z.ZodTypeAny, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.2" | undefined;
    manifest_version?: "0.2" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    privacy_policies?: string[] | undefined;
}, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.2" | undefined;
    manifest_version?: "0.2" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    privacy_policies?: string[] | undefined;
}>, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.2" | undefined;
    manifest_version?: "0.2" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    privacy_policies?: string[] | undefined;
}, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.2" | undefined;
    manifest_version?: "0.2" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    privacy_policies?: string[] | undefined;
}> | z.ZodEffects<z.ZodObject<{
    $schema: z.ZodOptional<z.ZodString>;
    dxt_version: z.ZodOptional<z.ZodLiteral<"0.3">>;
    manifest_version: z.ZodOptional<z.ZodLiteral<"0.3">>;
    name: z.ZodString;
    display_name: z.ZodOptional<z.ZodString>;
    version: z.ZodString;
    description: z.ZodString;
    long_description: z.ZodOptional<z.ZodString>;
    author: z.ZodObject<{
        name: z.ZodString;
        email: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    }, {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    }>;
    repository: z.ZodOptional<z.ZodObject<{
        type: z.ZodString;
        url: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        url: string;
        type: string;
    }, {
        url: string;
        type: string;
    }>>;
    homepage: z.ZodOptional<z.ZodString>;
    documentation: z.ZodOptional<z.ZodString>;
    support: z.ZodOptional<z.ZodString>;
    icon: z.ZodOptional<z.ZodString>;
    icons: z.ZodOptional<z.ZodArray<z.ZodObject<{
        src: z.ZodString;
        size: z.ZodString;
        theme: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        src: string;
        size: string;
        theme?: string | undefined;
    }, {
        src: string;
        size: string;
        theme?: string | undefined;
    }>, "many">>;
    screenshots: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    localization: z.ZodOptional<z.ZodObject<{
        resources: z.ZodString;
        default_locale: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        resources: string;
        default_locale: string;
    }, {
        resources: string;
        default_locale: string;
    }>>;
    server: z.ZodObject<{
        type: z.ZodEnum<["python", "node", "binary"]>;
        entry_point: z.ZodString;
        mcp_config: z.ZodObject<{
            command: z.ZodString;
            args: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
            env: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>;
        } & {
            platform_overrides: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodObject<{
                command: z.ZodOptional<z.ZodString>;
                args: z.ZodOptional<z.ZodOptional<z.ZodArray<z.ZodString, "many">>>;
                env: z.ZodOptional<z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodString>>>;
            }, "strict", z.ZodTypeAny, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }>>>;
        }, "strict", z.ZodTypeAny, {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        }, {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        }>;
    }, "strict", z.ZodTypeAny, {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    }, {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    }>;
    tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        name: string;
        description?: string | undefined;
    }, {
        name: string;
        description?: string | undefined;
    }>, "many">>;
    tools_generated: z.ZodOptional<z.ZodBoolean>;
    prompts: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
        arguments: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
        text: z.ZodString;
    }, "strict", z.ZodTypeAny, {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }, {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }>, "many">>;
    prompts_generated: z.ZodOptional<z.ZodBoolean>;
    keywords: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    license: z.ZodOptional<z.ZodString>;
    privacy_policies: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    compatibility: z.ZodOptional<z.ZodObject<{
        claude_desktop: z.ZodOptional<z.ZodString>;
        platforms: z.ZodOptional<z.ZodArray<z.ZodEnum<["darwin", "win32", "linux"]>, "many">>;
        runtimes: z.ZodOptional<z.ZodObject<{
            python: z.ZodOptional<z.ZodString>;
            node: z.ZodOptional<z.ZodString>;
        }, "strict", z.ZodTypeAny, {
            python?: string | undefined;
            node?: string | undefined;
        }, {
            python?: string | undefined;
            node?: string | undefined;
        }>>;
    }, "strict", z.ZodTypeAny, {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    }, {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    }>>;
    user_config: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodObject<{
        type: z.ZodEnum<["string", "number", "boolean", "directory", "file"]>;
        title: z.ZodString;
        description: z.ZodString;
        required: z.ZodOptional<z.ZodBoolean>;
        default: z.ZodOptional<z.ZodUnion<[z.ZodString, z.ZodNumber, z.ZodBoolean, z.ZodArray<z.ZodString, "many">]>>;
        multiple: z.ZodOptional<z.ZodBoolean>;
        sensitive: z.ZodOptional<z.ZodBoolean>;
        min: z.ZodOptional<z.ZodNumber>;
        max: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }>>>;
    _meta: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodRecord<z.ZodString, z.ZodAny>>>;
}, "strict", z.ZodTypeAny, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.3" | undefined;
    manifest_version?: "0.3" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
    privacy_policies?: string[] | undefined;
    icons?: {
        src: string;
        size: string;
        theme?: string | undefined;
    }[] | undefined;
    localization?: {
        resources: string;
        default_locale: string;
    } | undefined;
}, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.3" | undefined;
    manifest_version?: "0.3" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
    privacy_policies?: string[] | undefined;
    icons?: {
        src: string;
        size: string;
        theme?: string | undefined;
    }[] | undefined;
    localization?: {
        resources: string;
        default_locale: string;
    } | undefined;
}>, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.3" | undefined;
    manifest_version?: "0.3" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
    privacy_policies?: string[] | undefined;
    icons?: {
        src: string;
        size: string;
        theme?: string | undefined;
    }[] | undefined;
    localization?: {
        resources: string;
        default_locale: string;
    } | undefined;
}, {
    name: string;
    version: string;
    description: string;
    author: {
        name: string;
        email?: string | undefined;
        url?: string | undefined;
    };
    server: {
        type: "python" | "node" | "binary";
        entry_point: string;
        mcp_config: {
            command: string;
            args?: string[] | undefined;
            env?: Record<string, string> | undefined;
            platform_overrides?: Record<string, {
                command?: string | undefined;
                args?: string[] | undefined;
                env?: Record<string, string> | undefined;
            }> | undefined;
        };
    };
    $schema?: string | undefined;
    dxt_version?: "0.3" | undefined;
    manifest_version?: "0.3" | undefined;
    display_name?: string | undefined;
    long_description?: string | undefined;
    repository?: {
        url: string;
        type: string;
    } | undefined;
    homepage?: string | undefined;
    documentation?: string | undefined;
    support?: string | undefined;
    icon?: string | undefined;
    screenshots?: string[] | undefined;
    tools?: {
        name: string;
        description?: string | undefined;
    }[] | undefined;
    tools_generated?: boolean | undefined;
    prompts?: {
        name: string;
        text: string;
        description?: string | undefined;
        arguments?: string[] | undefined;
    }[] | undefined;
    prompts_generated?: boolean | undefined;
    keywords?: string[] | undefined;
    license?: string | undefined;
    compatibility?: {
        claude_desktop?: string | undefined;
        platforms?: ("darwin" | "win32" | "linux")[] | undefined;
        runtimes?: {
            python?: string | undefined;
            node?: string | undefined;
        } | undefined;
    } | undefined;
    user_config?: Record<string, {
        description: string;
        type: "string" | "number" | "boolean" | "directory" | "file";
        title: string;
        default?: string | number | boolean | string[] | undefined;
        min?: number | undefined;
        max?: number | undefined;
        required?: boolean | undefined;
        multiple?: boolean | undefined;
        sensitive?: boolean | undefined;
    }> | undefined;
    _meta?: Record<string, Record<string, any>> | undefined;
    privacy_policies?: string[] | undefined;
    icons?: {
        src: string;
        size: string;
        theme?: string | undefined;
    }[] | undefined;
    localization?: {
        resources: string;
        default_locale: string;
    } | undefined;
}>;
export {};
